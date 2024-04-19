from rest_framework import serializers

# Models
from domain.lead.models.Lead import Lead
from domain.system.models.Company import Company
from domain.lead.models.Status import Status

import logging
logger = logging.getLogger(__name__)



class ReadCompanySerializer(serializers.ModelSerializer):
    class Meta:
        # TODO: Add AI Documentation to use proper ref_name 
        ref_name = "agent.leads.ReadCompanySerializer"
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
        ref_name = "agent.leads.ReadStatusSerializer"
        model = Status
        fields = [
            'id',
            'status'
        ]


class ReadLeadSerializer(serializers.ModelSerializer):
    company = ReadCompanySerializer(read_only=True)
    status = ReadStatusSerializer(read_only=True)

    class Meta:
        ref_name = "agent.leads.ReadLeadSerializer"
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
            'last_message_at'
        ]

class CreateLeadSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = "agent.leads.CreateLeadSerializer"
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
        ref_name = "agent.leads.PaginateReadLeadSerializer"

    count = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()
    results = ReadLeadSerializer(many=True)


class PaginateQueryReadLeadSerializer(serializers.Serializer): # noqa

    class Meta:
        ref_name = "agent.leads.PaginateQueryReadLeadSerializer"

    page = serializers.IntegerField(required=False, help_text="A page number within the paginated result set.")
