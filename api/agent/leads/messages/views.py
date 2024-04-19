# DRF
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# Serializers
from .serializers import ReadLeadSerializer, \
    CreateLeadSerializer, PaginateReadLeadSerializer, \
    PaginateQueryReadLeadSerializer

# Services
from domain.lead.services.lead import get_leads_sorted_by_last_message_at

# Library: django-filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Library: django-filter
from domain.lead.filters.leads import LeadFilter


# Library: drf-yasg
from drf_yasg.utils import swagger_auto_schema

import logging
logger = logging.getLogger(__name__)


class LeadsMessagesAPIView(ListAPIView):

    # permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = LeadFilter
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'company__name', 'status__name']
    ordering_fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'company__name', 'status__name']
    serializer_class = ReadLeadSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return get_leads_sorted_by_last_message_at()

    @swagger_auto_schema(
        responses={
            200: PaginateReadLeadSerializer()
        },
        operation_description="This operation requires IsAuthenticated permission",
        operation_id="leads_message_list",
        tags=["agent.leads.messages"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

