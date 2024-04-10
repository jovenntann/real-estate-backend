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
from domain.lead.services.message import get_messages_by_lead

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
        return get_messages_by_lead(self.kwargs['lead_id'])

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
