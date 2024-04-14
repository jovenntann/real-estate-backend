
# Django
from django.utils import timezone
from django.http import HttpResponse

# DRF
from rest_framework.views import APIView
from rest_framework import status

# Services
from domain.system.services.company import get_company_by_id
from domain.facebook.services.page import get_page_by_page_id
from domain.lead.services.message import create_message, get_message_by_messenger_id
from domain.lead.services.lead import create_lead, get_lead_by_facebook_id, update_lead_last_message_at
from domain.lead.services.status import get_status_by_id

# Utilities
from domain.facebook.utils.facebook import get_message_by_message_id, get_user_profile_by_id

# Library: drf-yasg
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
logger = logging.getLogger(__name__)


class FacebookWebhookAPIView(APIView):

    @swagger_auto_schema(
        operation_description="This operation requires IsAuthenticated permission",
        operation_id="validate_token",
        tags=["webhook.facebook"],
        manual_parameters=[
            openapi.Parameter('hub_mode', openapi.IN_QUERY, description="Facebook's hub mode", type=openapi.TYPE_STRING),
            openapi.Parameter('hub_verify_token', openapi.IN_QUERY, description="Facebook's hub verify token", type=openapi.TYPE_STRING),
            openapi.Parameter('hub_challenge', openapi.IN_QUERY, description="Facebook's hub challenge", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request):
        logger.info(f"GET request received: {request.GET}")
        hub_mode = request.GET.get('hub.mode')
        hub_verify_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')

        if hub_mode == 'subscribe' and hub_verify_token == '09106850351':
            return HttpResponse(hub_challenge)
        return HttpResponse('Verification token mismatch', status=status.HTTP_403_FORBIDDEN)
        
    @swagger_auto_schema(
        operation_description="This operation requires IsAuthenticated permission",
        operation_id="events",
        tags=["webhook.facebook"],
    )
    def post(self, request, *args, **kwargs):
        logger.info(f"POST request body: {request.data}")

        entries = request.data.get('entry')

        # TODO: Get Company by Page ID
        company = get_company_by_id(id=1)
        
        for entry in entries:
            for messaging in entry.get('messaging', []):
                if 'message' in messaging: # Message from User
                    self.process_customer_message(company, messaging)
                elif 'delivery' in messaging: # Message from Page
                    self.process_page_message(company, messaging)
                            
        return HttpResponse('Success', status=status.HTTP_200_OK)

    def process_customer_message(self, company, messaging):
        page_id = messaging.get('recipient').get('id') # Page
        user_id = messaging.get('sender').get('id') # User
        page = get_page_by_page_id(page_id=page_id)

        # NOTE: Let's GET Message details from API so that processing of message are in same format
        message_details = get_message_by_message_id(page.access_token, messaging.get('message').get('mid'))

        # If Lead is not existing then create Lead
        lead = get_lead_by_facebook_id(facebook_id=message_details.data.sender.id)
        if lead is None:
            lead_status = get_status_by_id(id=1)
            user_profile = get_user_profile_by_id(access_token=page.access_token, user_id=message_details.data.sender.id)
            lead = create_lead(
                first_name=message_details.data.sender.name,
                last_name='',
                email=message_details.data.sender.email,
                phone_number='',
                company=company,
                status=lead_status,
                facebook_id=message_details.data.sender.id,
                facebook_profile_pic=user_profile.data.profile_pic if user_profile and user_profile.data else 'https://cdn.pixabay.com/photo/2013/07/13/10/44/man-157699_640.png'
            )
        # If Message is not existing then create Message
        message = get_message_by_messenger_id(messenger_id=message_details.data.id)
        if message is None:
            create_message(
                page=page,
                lead=lead,
                source='messenger',
                sender='lead',
                message=message_details.data.message,
                timestamp=timezone.now(),
                messenger_id=message_details.data.id,
                messenger_attachments=message_details.data.attachments,
                is_read=False
            )
        # Update Lead Last Message At
        update_lead_last_message_at(lead=lead, last_message_at=timezone.now())

    def process_page_message(self, company, messaging):
        page_id = messaging.get('recipient').get('id') # Page
        user_id = messaging.get('sender').get('id') # User
        page = get_page_by_page_id(page_id=page_id)
        message_ids = messaging.get('delivery').get('mids', [])
        
        for message_id in message_ids:
            # NOTE: Let's GET Message details from API so that processing of message are in same format
            message_details = get_message_by_message_id(page.access_token, message_id)
            page_id = message_details.data.sender.id
            page = get_page_by_page_id(page_id=page_id)
            sender_id = messaging.get('sender').get('id')
            logging.info(f"Delivered Message ID: {message_id}")
            
            # If Lead is not existing then create Lead
            lead = get_lead_by_facebook_id(facebook_id=sender_id)
            if lead is None:
                lead_status = get_status_by_id(id=1)
                user_profile = get_user_profile_by_id(access_token=page.access_token, user_id=message_details.data.recipient.data[0].id)
                lead = create_lead(
                    first_name=user_profile.data.first_name,
                    last_name=user_profile.data.last_name,
                    email=f"{sender_id}@facebook.com",
                    phone_number='',
                    company=company,
                    status=lead_status,
                    facebook_id=sender_id,
                    facebook_profile_pic=user_profile.data.profile_pic if user_profile and user_profile.data else 'https://cdn.pixabay.com/photo/2013/07/13/10/44/man-157699_640.png'
                )

             # If Message is not existing then create Message
            message = get_message_by_messenger_id(messenger_id=message_details.data.id)
            if message is None:
                create_message(
                    page=page,
                    lead=lead,
                    source='messenger',
                    sender='page',
                    message=message_details.data.message,
                    timestamp=timezone.now(),
                    messenger_id=message_details.data.id,
                    messenger_attachments=message_details.data.attachments,
                    is_read=True
                )
                update_lead_last_message_at(lead=lead, last_message_at=timezone.now())

