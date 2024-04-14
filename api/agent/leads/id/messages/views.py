# Django
from django.utils import timezone
from django.db.models import Q

# DRF
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# Serializers
from .serializers import ReadMessageSerializer, \
    CreateMessageSerializer, PaginateReadMessageSerializer, \
    PaginateQueryReadMessageSerializer, SendMessageSerializer

# Services
from domain.lead.services.lead import get_lead_by_id, update_lead_last_message_at
from domain.facebook.services.page import get_page_by_page_id
from domain.lead.services.message import get_messages_by_lead_id, create_message, mark_messages_as_read

# Utilities
from domain.facebook.utils.facebook import get_message_by_message_id, send_message


# Library: django-filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Library: django-filter
from domain.lead.filters.messages import MessageFilter

# Library: drf-yasg
from drf_yasg.utils import swagger_auto_schema

import logging
logger = logging.getLogger(__name__)


class LeadsIdMessagesAPIView(ListAPIView):

    # permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['page', 'lead', 'source', 'sender', 'messenger_id', 'message', 'timestamp']
    ordering_fields = ['id', 'page', 'lead', 'source', 'sender', 'messenger_id', 'message', 'timestamp']
    serializer_class = ReadMessageSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        messages = get_messages_by_lead_id(self.kwargs['lead_id'])
        mark_messages_as_read(messages)
        return messages

    @swagger_auto_schema(
        responses={
            200: PaginateReadMessageSerializer()
        },
        operation_description="This operation requires IsAuthenticated permission",
        operation_id="lead_messages_list",
        tags=["agent.lead_messages"],
    )
    def get(self, request, *args, **kwargs):

        return super().get(request, *args, **kwargs)

    @staticmethod
    @swagger_auto_schema(
        request_body=SendMessageSerializer,
        operation_description="This operation requires IsAuthenticated permission",
        operation_id="lead_messages_create",
        tags=["agent.lead_messages"],
        responses={
            200: ReadMessageSerializer()
        }
    )
    def post(request, lead_id=None, *args, **kwargs):
        logger.info(f"authenticated: {request.user}")
        message_serializer = SendMessageSerializer(data=request.data)
        message_serializer.is_valid(raise_exception=True)

        lead = get_lead_by_id(lead_id=lead_id)

        # NOTE: No need to get this since we serialized it with Model serializer
        # page = get_page_by_page_id(page_id=message_serializer.validated_data['page'])

        # Send Message API
        message_response = send_message(
            access_token=message_serializer.validated_data['page'].access_token,
            recipient_id=lead.facebook_id,
            message=message_serializer.validated_data['message'],
            tag='POST_PURCHASE_UPDATE'
        )
        # Get Message API
        message_detail = get_message_by_message_id(
            access_token=message_serializer.validated_data['page'].access_token,
            message_id=message_response.data.message_id,
        )

        message = create_message(
            page=message_serializer.validated_data['page'],
            lead=lead,
            source=message_serializer.validated_data['source'],
            sender=message_serializer.validated_data['sender'],
            message=message_detail.data.message,
            timestamp=timezone.now(),
            messenger_id=message_response.data.message_id,
            messenger_attachments=message_detail.data.attachments,
            is_read=True
        )
        update_lead_last_message_at(lead=lead, last_message_at=timezone.now())
        message_serializer = ReadMessageSerializer(message)

        return Response(message_serializer.data)
