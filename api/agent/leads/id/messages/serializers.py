from rest_framework import serializers

# Models
from domain.lead.models.Message import Message

class ReadMessageSerializer(serializers.ModelSerializer):
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
