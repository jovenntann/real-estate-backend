from rest_framework import serializers

# Models
from domain.lead.models.Message import Message
from domain.lead.models.Lead import Lead
from domain.facebook.models.Page import Page


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'company',
            'status',
            'facebook_id'
        ]

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = [
            'id',
            'page_name',
            'page_id',
        ]


class ReadMessageSerializer(serializers.ModelSerializer):

    page = PageSerializer(read_only=True)
    lead = LeadSerializer(read_only=True)

    class Meta:
        ref_name = "agent.leads.id.message.ReadMessageSerializer"
        model = Message
        fields = [
            'id',
            'page',
            'lead',
            'source',
            'sender',
            'messenger_id',
            'message',  
            'messenger_attachments',
            'is_read',
            'timestamp'
        ]

class CreateMessageSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = "agent.leads.id.message.CreateMessageSerializer"
        model = Message
        fields = [
            'page',
            'lead',
            'source',
            'sender',
            'message',
            'timestamp',
            'messenger_id'
        ]

class PaginateReadMessageSerializer(serializers.Serializer): 

    class Meta:
        ref_name = "agent.leads.id.message.PaginateReadMessageSerializer"

    count = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()
    results = ReadMessageSerializer(many=True)


class PaginateQueryReadMessageSerializer(serializers.Serializer): 

    class Meta:
        ref_name = "agent.leads.id.message.PaginateQueryReadMessageSerializer"

    page = serializers.IntegerField(required=False, help_text="A page number within the paginated result set.")
