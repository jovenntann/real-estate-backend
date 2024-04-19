from rest_framework import serializers

# Models
from domain.system.models.Company import Company
from domain.lead.models.Status import Status
from domain.lead.models.MessageStatus import MessageStatus
from domain.lead.models.NextAction import NextAction

import logging
logger = logging.getLogger(__name__)


class ReadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "agent.system.company.ReadStatusSerializer"
        model = Status
        fields = ['id', 'status', 'description', 'color']


class ReadMessageStatusSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "agent.system.company.ReadMessageStatusSerializer"
        model = MessageStatus
        fields = ['id', 'status', 'description']


class ReadNextActionSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "agent.system.company.ReadNextActionSerializer"
        model = NextAction
        fields = ['id', 'action', 'description', 'color']


class ReadCompanySerializer(serializers.ModelSerializer):
    lead_statuses = ReadStatusSerializer(many=True, read_only=True)
    lead_message_statuses = ReadMessageStatusSerializer(many=True, read_only=True)
    lead_next_actions = ReadNextActionSerializer(many=True, read_only=True)

    class Meta:
        ref_name = "agent.system.company.ReadCompanySerializer"
        model = Company
        fields = [
            'id',
            'company_name',
            'address',
            'phone_number',
            'company_size',
            'industry',
            'lead_statuses',
            'lead_message_statuses',
            'lead_next_actions'
        ]
