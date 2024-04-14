from rest_framework import serializers

# Models
from domain.lead.models.Message import Message
from domain.lead.models.Lead import Lead
from domain.facebook.models.Page import Page


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "webhook.facebook.LeadSerializer"
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
        ref_name = "webhook.facebook.PageSerializer"
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
        ref_name = "webhook.facebook.ReadMessageSerializer"
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
