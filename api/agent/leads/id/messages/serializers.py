from rest_framework import serializers

# Models
from domain.lead.models.Message import Message
from domain.lead.models.Lead import Lead
from domain.facebook.models.Page import Page
from domain.lead.models.Status import Status
from domain.lead.models.NextAction import NextAction



class ReadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "agent.leads.id.message.ReadStatusSerializer"
        model = Status
        fields = [
            'id',
            'status',
            'color',
            'description'
        ]


class ReadNextActionSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "agent.leads.id.message.ReadNextActionSerializer"
        model = NextAction
        fields = [
            'id',
            'action',
            'color',
            'description'
        ]



class LastMessageSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = "agent.leads.id.message.LastMessageSerializer"
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


class LeadSerializer(serializers.ModelSerializer):

    status = ReadStatusSerializer(read_only=True)
    next_action = ReadNextActionSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        ref_name = "agent.leads.id.message.LeadSerializer"
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

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-timestamp').first()
        if last_message:
            return LastMessageSerializer(last_message).data
        return None


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


class SendMessageSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = "agent.leads.id.message.CreateMessageSerializer"
        model = Message
        fields = [
            'page',
            'source',
            'sender',
            'message',
        ]