from rest_framework import serializers


class FacebookWebhookSerializer(serializers.Serializer):
    hub_mode = serializers.CharField(max_length=50)
    hub_verify_token = serializers.CharField(max_length=50)
    hub_challenge = serializers.CharField(max_length=50)

    class Meta:
        ref_name = "webhook.facebook.FacebookWebhookSerializer"
