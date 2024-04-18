
# Django
from django.utils import timezone
from django.http import HttpResponse

# DRF
from rest_framework.views import APIView
from rest_framework import status

from .serializers import ReadMessageSerializer

# Services
from domain.system.services.company import get_company_by_id
from domain.facebook.services.page import get_page_by_page_id
from domain.lead.services.message import create_message, get_message_by_messenger_id, get_message_by_id
from domain.lead.services.lead import create_lead, get_lead_by_facebook_id, update_lead_last_message_at
from domain.lead.services.status import get_status_by_id

# Service: Automation
from domain.facebook.services.sequence import get_sequence_by_id
from domain.facebook.services.template import get_templates_by_sequence_order

# Utilities
from domain.facebook.utils.facebook import get_message_by_message_id, get_user_profile_by_id, send_template_message
from domain.pusher.utils.pusher import send_pusher_notification

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
                # events: message_echoes
                if 'message' in messaging and messaging['message'].get('is_echo', False): # Message from Page
                    page_id = messaging.get('sender').get('id')
                    user_id = messaging.get('recipient').get('id')
                    message_ids = [messaging['message'].get('mid')]
                    self.process_page_message(company, message_ids, page_id, user_id)
                # events: messaging
                elif 'message' in messaging: # Message from User
                    self.process_customer_message(company, messaging)
                elif 'delivery' in messaging: # Message from Page
                    page_id = messaging.get('recipient').get('id')
                    user_id = messaging.get('sender').get('id')
                    message_ids = messaging.get('delivery').get('mids', [])
                    self.process_page_message(company, message_ids, page_id, user_id)
                            
        return HttpResponse('Success', status=status.HTTP_200_OK)
    
    # TODO: Handle Sticker Message (Because getting from Get Message ID doesn't return Attachments and it's just an empty Message)

    def process_customer_message(self, company, messaging):
        # TODO: Handling of Emoticon E.g thumbs-up
        page_id = messaging.get('recipient').get('id') # Page
        user_id = messaging.get('sender').get('id') # User
        page = get_page_by_page_id(page_id=page_id)

        # TODO: Check if Message exist using get_message_by_id(message_id=messaging.get('message').get('mid'))
        # Logs and then Return

        # NOTE: Let's GET Message details from API so that processing of message are in same format
        message_details = get_message_by_message_id(page.access_token, messaging.get('message').get('mid'))

        # If Lead is not existing then create Lead
        lead = get_lead_by_facebook_id(facebook_id=message_details.data.sender.id)
        if lead is None:
            user_profile = get_user_profile_by_id(access_token=page.access_token, user_id=message_details.data.sender.id)
            # TODO: Set default value for this
            lead_status = get_status_by_id(id=1)
            message_status = None
            next_action = None
            lead = create_lead(
                first_name=user_profile.data.first_name,
                last_name=user_profile.data.last_name,
                email=f"{user_profile.data.id}@facebook.com",
                phone_number='',
                company=company,
                status=lead_status,
                facebook_id=message_details.data.sender.id,
                facebook_profile_pic=user_profile.data.profile_pic if user_profile and user_profile.data else 'https://cdn.pixabay.com/photo/2013/07/13/10/44/man-157699_640.png',
                message_status=message_status,
                next_action=next_action
            )
        # If Message is not existing then create Message
        message = get_message_by_messenger_id(messenger_id=message_details.data.id)
        if message is None:
            created_message = create_message(
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

            # Send to Pusher
            message_serializer = ReadMessageSerializer(created_message)        
            channel = f"my-channel"
            event = "new-message"
            data = message_serializer.data
            send_pusher_notification(channel, event, data)

            # Update Lead Last Message At
            update_lead_last_message_at(lead=lead, last_message_at=timezone.now())

            # Process automation
            if message_details.data.message == 'details':
                # TODO: Get sequence by Keywords: Pililla Hulo Rizal
                sequence = get_sequence_by_id(id=1)
                templates = get_templates_by_sequence_order(sequence=sequence)
                for template in templates:
                    send_template_message_response = send_template_message(
                        user_id=message_details.data.sender.id,
                        template_content=template.template_content,
                        delay=template.delay,
                        access_token=page.access_token
                    )

    def process_page_message(self, company, message_ids, page_id, user_id):
        page = get_page_by_page_id(page_id=page_id)
        
        for message_id in message_ids:
            # NOTE: Let's GET Message details from API so that processing of message are in same format
            message_details = get_message_by_message_id(page.access_token, message_id)
            page_id = message_details.data.sender.id
            page = get_page_by_page_id(page_id=page_id)
            logging.info(f"Delivered Message ID: {message_id}")
            
            # If Lead is not existing then create Lead
            lead = get_lead_by_facebook_id(facebook_id=user_id)
            if lead is None:
                user_profile = get_user_profile_by_id(access_token=page.access_token, user_id=message_details.data.recipient.data[0].id)
                # TODO: Set default value for this
                lead_status = get_status_by_id(id=1)
                message_status = None
                next_action = None
                lead = create_lead(
                    first_name=user_profile.data.first_name,
                    last_name=user_profile.data.last_name,
                    email=f"{user_profile.data.id}@facebook.com",
                    phone_number='',
                    company=company,
                    status=lead_status,
                    facebook_id=message_details.data.sender.id,
                    facebook_profile_pic=user_profile.data.profile_pic if user_profile and user_profile.data else 'https://cdn.pixabay.com/photo/2013/07/13/10/44/man-157699_640.png',
                    message_status=message_status,
                    next_action=next_action
                )
             # If Message is not existing then create Message
            message = get_message_by_messenger_id(messenger_id=message_details.data.id)
            if message is None:
                created_message = create_message(
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

                # Send to Pusher
                message_serializer = ReadMessageSerializer(created_message)        
                channel = f"my-channel"
                event = "new-message"
                data = message_serializer.data
                send_pusher_notification(channel, event, data)
                
                update_lead_last_message_at(lead=lead, last_message_at=timezone.now())

                # TODO: Process automation as Page (Handler for message sent from Facebook Page)
                # NOTE: This might become duplicate of code on the send message backend api endpoint || No need this should be sent over the API select Sequence :)
                if message_details.data.message == '#details':
                    # TODO: Get sequence by Keywords: Pililla Hulo Rizal
                    sequence = get_sequence_by_id(id=1)
                    templates = get_templates_by_sequence_order(sequence=sequence)
                    for template in templates:
                        send_template_message_response = send_template_message(
                            user_id=user_id,
                            template_content=template.template_content,
                            delay=template.delay,
                            access_token=page.access_token
                        )
                        logger.info(f"Sent template message with id {template.id} and response: {send_template_message_response.data}")
