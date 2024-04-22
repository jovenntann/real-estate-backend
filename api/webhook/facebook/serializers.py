from rest_framework import serializers

# Models
from domain.lead.models.Message import Message
from domain.lead.models.Lead import Lead
from domain.facebook.models.Page import Page
from domain.lead.models.Status import Status
from domain.lead.models.NextAction import NextAction


class ReadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "agent.leads.messages.ReadStatusSerializer"
        model = Status
        fields = [
            'id',
            'status',
            'color',
            'description'
        ]


class ReadNextActionSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "agent.leads.messages.ReadNextActionSerializer"
        model = NextAction
        fields = [
            'id',
            'action',
            'color',
            'description'
        ]


class LeadSerializer(serializers.ModelSerializer):

    status = ReadStatusSerializer(read_only=True)
    next_action = ReadNextActionSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()

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
            'next_action',
            'facebook_id',
            'facebook_profile_pic',
            'last_message_at',
            'last_message'
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
