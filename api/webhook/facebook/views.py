
# Django
import datetime
from django.http import HttpResponse

# DRF
from rest_framework.views import APIView
from rest_framework import status

# Services
from domain.facebook.services.page import get_page_by_page_id
from domain.lead.services.message import create_message

# Utilities
from domain.facebook.utils.facebook import get_message_by_message_id

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
        
        for entry in entries:
            for messaging in entry.get('messaging', []):
                if 'message' in messaging:
                    logging.info("Message from Customer")
                    sender_id = messaging.get('sender').get('id')
                    logging.info(f"Sender ID: {sender_id}")
                    recipient_id = messaging.get('recipient').get('id')
                    logging.info(f"Recipient ID: {recipient_id}")
                elif 'delivery' in messaging:
                    logging.info("Message from Page")
                    sender_id = messaging.get('sender').get('id')
                    logging.info(f"Sender ID: {sender_id}")
                    recipient_id = messaging.get('recipient').get('id')
                    logging.info(f"Recipient ID: {recipient_id}")


        # entries = request.data.get('entry')
        # for entry in entries:
        #     messagings = entry.get('messaging')
        #     for messaging in messagings:
        #         page_id = messaging.get('sender').get('id')
        #         message = messaging.get('message').get('text')
        #         timestamp = messaging.get('timestamp')
        #         timestamp = datetime.datetime.fromtimestamp(timestamp / 1000, tz=datetime.timezone.utc)

        #         page = get_page_by_page_id(page_id=page_id)

        #         create_message(
        #             page=page,
        #             lead=None,
        #             source='facebook',
        #             sender='lead',
        #             message=message,
        #             timestamp=timestamp,
        #             messenger_id=None,
        #             messenger_attachments=None,
        #             is_read=False
        #         )

        # return HttpResponse()

        return HttpResponse('Success', status=status.HTTP_200_OK)
