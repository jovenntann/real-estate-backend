
# DRF
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Serializers
from .serializers import ReadLeadSerializer, \
    UpdateLeadSerializer, DeleteLeadSerializer

# Services
from domain.lead.services.lead import get_lead_by_id, delete_lead, update_lead

# Django Shortcuts
from django.shortcuts import get_object_or_404
from django.http import Http404

# Library: drf-yasg
from drf_yasg.utils import swagger_auto_schema

import logging
logger = logging.getLogger(__name__)


class LeadIdAPIView(APIView):

    # permission_classes = (IsAdminOrHumanResource,)

    @staticmethod
    @swagger_auto_schema(
        responses={
            200: ReadLeadSerializer()
        },
        # operation_description=f"This operation requires {permission_classes} permission",
        operation_id="leads_read",
        tags=["agent.leads.id"],
    )
    def get(request, lead_id=None):
        logger.info(f"authenticated: {request.user}")
        lead = get_lead_by_id(lead_id)
        if lead is None:
            raise Http404
        lead_serializer = ReadLeadSerializer(lead)
        return Response(lead_serializer.data)

    @staticmethod
    @swagger_auto_schema(
        # operation_description=f"This operation requires {permission_classes} permission",
        operation_id="leads_delete",
        tags=["agent.leads.id"],
        responses={
            200: DeleteLeadSerializer()
        }
    )
    def delete(request, lead_id=None):
        logger.info(f"authenticated: {request.user}")
        lead = get_lead_by_id(lead_id)
        if lead is None:
            raise Http404
        # Copy lead so that we can return this data from our delete response
        response = {
            'operation': 'delete',
            'domain': 'lead_management',
            'model': 'Lead',
            'data': lead
        }
        response_serializer = DeleteLeadSerializer(response)
        response_serializer_data = response_serializer.data

        delete_lead(lead)

        return Response(response_serializer_data)

    @staticmethod
    @swagger_auto_schema(
        # operation_description=f"This operation requires {permission_classes} permission",
        operation_id="leads_update",
        tags=["agent.leads.id"],
        request_body=UpdateLeadSerializer,
        responses={
            200: ReadLeadSerializer()
        }
    )
    def put(request, lead_id=None):
        logger.info(f"authenticated: {request.user}")

        lead = get_lead_by_id(lead_id)

        if lead is None:
            raise Http404

        lead_serializer = UpdateLeadSerializer(data=request.data)
        lead_serializer.is_valid(raise_exception=True)

        update_lead(
            lead=lead,
            # Can only update
            new_first_name=lead_serializer.validated_data.get('first_name', lead.first_name),
            new_last_name=lead_serializer.validated_data.get('last_name', lead.last_name),
            new_email=lead_serializer.validated_data.get('email', lead.email),
            new_phone_number=lead_serializer.validated_data.get('phone_number', lead.phone_number),
            new_status=lead_serializer.validated_data.get('status', lead.status),
            new_message_status=lead_serializer.validated_data.get('message_status', lead.message_status),
            new_next_action=lead_serializer.validated_data.get('next_action', lead.next_action)
        )
        # NOTE: Re-serialize to fetch more detailed data
        lead_serializer = ReadLeadSerializer(lead)
        return Response(lead_serializer.data)

    @staticmethod
    @swagger_auto_schema(
        # operation_description=f"This operation requires {permission_classes} permission",
        operation_id="leads_patch",
        tags=["agent.leads.id"],
        request_body=UpdateLeadSerializer,
        responses={
            200: ReadLeadSerializer()
        }
    )
    def patch(request, lead_id=None):
        logger.info(f"authenticated: {request.user}")

        lead = get_lead_by_id(lead_id)
        if lead is None:
            raise Http404

        lead_serializer = UpdateLeadSerializer(data=request.data)
        lead_serializer.is_valid(raise_exception=True)

        update_lead(
            lead=lead,
            # Can only update based on serializer
            new_first_name=lead_serializer.validated_data.get('first_name', lead.first_name),
            new_last_name=lead_serializer.validated_data.get('last_name', lead.last_name),
            new_email=lead_serializer.validated_data.get('email', lead.email),
            new_phone_number=lead_serializer.validated_data.get('phone_number', lead.phone_number),
            new_status=lead_serializer.validated_data.get('status', lead.status),
            new_message_status=lead_serializer.validated_data.get('message_status', lead.message_status),
            new_next_action=lead_serializer.validated_data.get('next_action', lead.next_action)
        )
        # NOTE: Re-serialize to fetch more detailed data
        lead_serializer = ReadLeadSerializer(lead)
        return Response(lead_serializer.data)


