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
from domain.lead.services.lead import get_leads, create_lead

# Library: django-filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Library: django-filter
from domain.lead.filters.leads import LeadFilter


# Library: drf-yasg
from drf_yasg.utils import swagger_auto_schema

import logging
logger = logging.getLogger(__name__)


class LeadsAPIView(ListAPIView):

    # permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = LeadFilter
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'company__name', 'status__name']
    ordering_fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'company__name', 'status__name']
    serializer_class = ReadLeadSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return get_leads()

    @swagger_auto_schema(
        responses={
            200: PaginateReadLeadSerializer()
        },
        operation_description="This operation requires IsAuthenticated permission",
        operation_id="leads_list",
        tags=["agent.leads"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @staticmethod
    @swagger_auto_schema(
        request_body=CreateLeadSerializer,
        operation_description="This operation requires IsAuthenticated permission",
        operation_id="leads_create",
        tags=["agent.leads"],
        responses={
            200: ReadLeadSerializer()
        }
    )
    def post(request, pk=None, *args, **kwargs):
        logger.info(f"authenticated: {request.user}")
        lead_serializer = CreateLeadSerializer(data=request.data)
        lead_serializer.is_valid(raise_exception=True)
        lead = create_lead(
            lead_serializer.validated_data['first_name'], 
            lead_serializer.validated_data['last_name'], 
            lead_serializer.validated_data['email'], 
            lead_serializer.validated_data['phone_number'], 
            lead_serializer.validated_data['company'], 
            lead_serializer.validated_data['status']
        )
        lead_serializer = ReadLeadSerializer(lead)

        return Response(lead_serializer.data)

