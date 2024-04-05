from rest_framework import serializers

# Models
from domain.lead.models.Lead import Lead

import logging
logger = logging.getLogger(__name__)


class ReadLeadSerializer(serializers.ModelSerializer):
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
            'status'
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
