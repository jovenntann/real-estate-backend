from rest_framework import serializers

# Models
from domain.lead.models.Message import Message
from domain.lead.models.Lead import Lead
from domain.facebook.models.Page import Page

import logging
logger = logging.getLogger(__name__)

class ReadPageSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "agent.messages.ReadPageSerializer"
        model = Page
        fields = [
            'id',
            'page_name',
            'page_id',
            'access_token'
        ]

class ReadLeadSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "agent.messages.ReadLeadSerializer"
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

class ReadMessageSerializer(serializers.ModelSerializer):
    page = ReadPageSerializer(read_only=True)
    lead = ReadLeadSerializer(read_only=True)

    class Meta:
        ref_name = "agent.messages.ReadMessageSerializer"
        model = Message
        fields = [
            'id',
            'page',
            'lead',
            'source',
            'sender',
            'messenger_id',
            'message',
            'timestamp'
        ]

class CreateMessageSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = "agent.messages.CreateMessageSerializer"
        model = Message
        fields = [
            'page',
            'lead',
            'source',
            'sender',
            'messenger_id',
            'message',
            'timestamp'
        ]

class PaginateReadMessageSerializer(serializers.Serializer): # noqa

    class Meta:
        ref_name = "agent.messages.PaginateReadMessageSerializer"

    count = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()
    results = ReadMessageSerializer(many=True)


class PaginateQueryReadMessageSerializer(serializers.Serializer): # noqa

    class Meta:
        ref_name = "agent.messages.PaginateQueryReadMessageSerializer"

    page = serializers.IntegerField(required=False, help_text="A page number within the paginated result set.")

