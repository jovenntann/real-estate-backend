from rest_framework import serializers

# Models
from domain.lead.models.Lead import Lead
from domain.system.models.Company import Company
from domain.lead.models.Status import Status
from domain.lead.models.Message import Message

import logging
logger = logging.getLogger(__name__)


class ReadMessageSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "agent.leads.messages.ReadMessageSerializer"
        model = Message
        fields = [
            'id',
            'source',
            'sender',
            'message',
            'is_read',
            'timestamp'
        ]


class ReadCompanySerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "agent.leads.messages.ReadCompanySerializer"
        model = Company
        fields = [
            'id',
            'company_name',
            'address',
            'phone_number',
            'company_size',
            'industry'
        ]


class ReadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "agent.leads.messages.ReadStatusSerializer"
        model = Status
        fields = [
            'id',
            'status',
            'color'
        ]


class ReadLeadSerializer(serializers.ModelSerializer):
    company = ReadCompanySerializer(read_only=True)
    status = ReadStatusSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        ref_name = "agent.leads.messages.ReadLeadSerializer"
        model = Lead
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'company',
            'status',
            'facebook_id',
            'facebook_profile_pic',
            'last_message_at',
            'last_message'
        ]

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-timestamp').first()
        if last_message:
            return ReadMessageSerializer(last_message).data
        return None

class CreateLeadSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = "agent.leads.messages.CreateLeadSerializer"
        model = Lead
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'company',
            'status'
        ]


class PaginateReadLeadSerializer(serializers.Serializer): # noqa

    class Meta:
        ref_name = "agent.leads.messages.PaginateReadLeadSerializer"

    count = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()
    results = ReadLeadSerializer(many=True)


class PaginateQueryReadLeadSerializer(serializers.Serializer): # noqa

    class Meta:
        ref_name = "agent.leads.messages.PaginateQueryReadLeadSerializer"

    page = serializers.IntegerField(required=False, help_text="A page number within the paginated result set.")
