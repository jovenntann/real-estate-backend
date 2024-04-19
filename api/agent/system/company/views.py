
# DRF
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Serializers
from .serializers import ReadCompanySerializer

# Services
from domain.system.services.company import get_company_by_id

# Django Shortcuts
from django.http import Http404

# Library: drf-yasg
from drf_yasg.utils import swagger_auto_schema

import logging
logger = logging.getLogger(__name__)


class AgentSystemCompanyAPIView(APIView):

    # permission_classes = (IsAuthenticated,)

    @staticmethod
    @swagger_auto_schema(
        responses={
            200: ReadCompanySerializer()
        },
        # operation_description=f"This operation requires {permission_classes} permission",
        operation_id="company_read",
        tags=["agent.system.company"],
    )
    def get(request):
        logger.info(f"authenticated: {request.user}")
        # TODO: Get Company by Authenticated User
        company = get_company_by_id(id=1)
        if company is None:
            raise Http404
        company_serializer = ReadCompanySerializer(company)
        return Response(company_serializer.data)
