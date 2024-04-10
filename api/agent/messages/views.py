
# Django
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
    PaginateQueryReadMessageSerializer

# Services
from domain.lead.services.message import get_messages, create_message

# Library: django-filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Library: django-filter
from domain.lead.filters.messages import MessageFilter

# Library: drf-yasg
from drf_yasg.utils import swagger_auto_schema

import logging
logger = logging.getLogger(__name__)


class MessagesAPIView(ListAPIView):

    # permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['page', 'lead', 'source', 'sender', 'messenger_id', 'message', 'timestamp']
    ordering_fields = ['id', 'page', 'lead', 'source', 'sender', 'messenger_id', 'message', 'timestamp']
    serializer_class = ReadMessageSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return get_messages()

    @swagger_auto_schema(
        responses={
            200: PaginateReadMessageSerializer()
        },
        operation_description="This operation requires IsAuthenticated permission",
        operation_id="messages_list",
        tags=["agent.messages"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    # @staticmethod
    # @swagger_auto_schema(
    #     request_body=CreateMessageSerializer,
    #     operation_description="This operation requires IsAuthenticated permission",
    #     operation_id="messages_create",
    #     tags=["agent.messages"],
    #     responses={
    #         200: ReadMessageSerializer()
    #     }
    # )
    # def post(request, pk=None, *args, **kwargs):
    #     logger.info(f"authenticated: {request.user}")
    #     message_serializer = CreateMessageSerializer(data=request.data)
    #     message_serializer.is_valid(raise_exception=True)
    #     message = create_message(message_serializer.validated_data['page'], message_serializer.validated_data['lead'], message_serializer.validated_data['source'], message_serializer.validated_data['sender'], message_serializer.validated_data['message'], message_serializer.validated_data['timestamp'], message_serializer.validated_data['messenger_id'])
    #     message_serializer = ReadMessageSerializer(message)

    #     return Response(message_serializer.data)

