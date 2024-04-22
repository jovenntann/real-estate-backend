from rest_framework import serializers

# Models
from domain.lead.models.Lead import Lead
from domain.system.models.Company import Company
from domain.lead.models.Status import Status
from domain.lead.models.NextAction import NextAction
from domain.lead.models.MessageStatus import MessageStatus

import logging
logger = logging.getLogger(__name__)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name', 'address', 'phone_number', 'company_size', 'industry']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'status', 'description', 'color']


class NextActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextAction
        fields = ['id', 'action', 'description', 'color']


class MessageStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageStatus
        fields = ['id', 'status', 'description']


class ReadLeadSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    status = StatusSerializer()
    next_action = NextActionSerializer()
    message_status = MessageStatusSerializer()

    class Meta:
        ref_name = "agent.leads.id.ReadLeadSerializer"
        model = Lead
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'company',
            'status',
            'next_action',
            'facebook_id',
            'facebook_profile_pic',
            'last_message_at',
            'message_status'
        ]


class UpdateLeadSerializer(serializers.ModelSerializer):
    # BUG FIX: "lead with this email already exists."
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        ref_name = "agent.leads.id.UpdateLeadSerializer"
        model = Lead
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'status',
            'next_action'
        ]

class DeleteLeadSerializer(serializers.Serializer): # noqa

    class Meta:
        ref_name = "agent.leads.id.DeleteLeadSerializer"

    operation = serializers.CharField(max_length=100)
    domain = serializers.CharField(max_length=200)
    model = serializers.CharField(max_length=100)
    data = ReadLeadSerializer()

