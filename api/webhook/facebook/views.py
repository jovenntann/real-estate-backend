
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

# Serializer
from .serializers import FacebookWebhookSerializer

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
        # Facebook webhook verification
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

        # Customer send message to Page Example:
        # Chat: {'object': 'page', 'entry': [{'time': 1712997933323, 'id': '113575558420278', 'messaging': [{'sender': {'id': '7009285825754582'}, 'recipient': {'id': '113575558420278'}, 'timestamp': 1712997932821, 'message': {'mid': 'm_vAs51ROH_-zLSM0bbzRq6FurOkQo4BOZ_duwjZMJl4SJEoA6XwYUT7CNlXHfwQKwbV3LLpVfX0MkxI7Bl_NvMg', 'text': 'chat from customer'}}]}]}
        # Photo: {'object': 'page', 'entry': [{'time': 1712998011760, 'id': '113575558420278', 'messaging': [{'sender': {'id': '7009285825754582'}, 'recipient': {'id': '113575558420278'}, 'timestamp': 1712998010990, 'message': {'mid': 'm_daLBS6EYcpo5ng-425GHylurOkQo4BOZ_duwjZMJl4TWoVYV-IzK9XiHZB36KjLgxZuczuuhXGSMDUK5zqfkhA', 'attachments': [{'type': 'image', 'payload': {'url': 'https://scontent.xx.fbcdn.net/v/t1.15752-9/434290628_1126044781950234_7585715723277066278_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=5f2048&_nc_ohc=QQuuMZATdJMAb63ZIjU&_nc_ad=z-m&_nc_cid=0&_nc_ht=scontent.xx&oh=03_AdVvbUa3qCHUvghqkcHbI1-_rlOSCbVWhwVFt1MOaMHBpQ&oe=6641A1FE'}}]}}]}]}

        # Page send message to Customer  Example:
        # {'object': 'page', 'entry': [{'time': 1712997890540, 'id': '113575558420278', 'messaging': [{'sender': {'id': '7009285825754582'}, 'recipient': {'id': '113575558420278'}, 'timestamp': 1712997890264, 'delivery': {'mids': ['m_W7KaTyconZFw_3X490iCElurOkQo4BOZ_duwjZMJl4Q77tkbf_5SADdc0FE_FL9EqI1hucPuTHzI-pjuRocVTw'], 'watermark': 1712997889147}}]}]}

        logger.info(f"POST request body: {request.data}")

        entries = request.data.get('entry')

        company = get_company_by_id(id=1)
        page = get_page_by_page_id(page_id=113575558420278)
        
        for entry in entries:
            for messaging in entry.get('messaging', []):
                if 'message' in messaging:
                    logging.info("Message from Customer")
                    sender_id = messaging.get('sender').get('id')
                    logging.info(f"Sender ID: {sender_id}")
                    recipient_id = messaging.get('recipient').get('id')
                    logging.info(f"Recipient ID: {recipient_id}")

                    message_id = messaging.get('message').get('mid')
                    logging.info(f"Message ID: {message_id}")

                    message_details = get_message_by_message_id(page.access_token, message_id)

                    lead = get_lead_by_facebook_id(facebook_id=message_details.data.sender.id)
                    if lead is None:
                        laad_status = get_status_by_id(id=1)
                        user_profile = get_user_profile_by_id(access_token=page.access_token, user_id=message_details.data.sender.id)
                        lead = create_lead(
                            first_name=message_details.data.sender.name,
                            last_name='',
                            email=message_details.data.sender.email,
                            phone_number='',
                            company=company,
                            status=laad_status,
                            facebook_id=message_details.data.sender.id,
                            facebook_profile_pic=user_profile.data.profile_pic if user_profile and user_profile.data else 'https://cdn.pixabay.com/photo/2013/07/13/10/44/man-157699_640.png'
                        )

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
                    update_lead_last_message_at(lead=lead, last_message_at=timezone.now())

                elif 'delivery' in messaging:
                    logging.info("Message from Page")
                    sender_id = messaging.get('sender').get('id') # User
                    logging.info(f"Sender ID: {sender_id}")
                    recipient_id = messaging.get('recipient').get('id') # Page
                    logging.info(f"Recipient ID: {recipient_id}")
                    message_ids = messaging.get('delivery').get('mids')
                    
                    for message_id in message_ids:
                        logging.info(f"Delivered Message ID: {message_id}")
                        message_details = get_message_by_message_id(page.access_token, message_id)

                        lead = get_lead_by_facebook_id(facebook_id=sender_id)
                        if lead is None:
                            laad_status = get_status_by_id(id=1)
                            user_profile = get_user_profile_by_id(access_token=page.access_token, user_id=sender_id)
                            lead = create_lead(
                                first_name=user_profile.data.first_name,
                                last_name=user_profile.data.last_name,
                                email=f"{sender_id}@facebook.com",
                                phone_number='',
                                company=company,
                                status=laad_status,
                                facebook_id=sender_id,
                                facebook_profile_pic=user_profile.data.profile_pic if user_profile and user_profile.data else 'https://cdn.pixabay.com/photo/2013/07/13/10/44/man-157699_640.png'
                            )
                        # Let's also create record for Lead Message if not existing
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
                                is_read=False
                            )
                            update_lead_last_message_at(lead=lead, last_message_at=timezone.now())
                            
        # return HttpResponse()

        return HttpResponse('Success', status=status.HTTP_200_OK)
