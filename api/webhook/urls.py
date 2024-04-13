from django.urls import path

# Views
from .facebook.views import FacebookWebhookAPIView

urlpatterns = [
    path('facebook', FacebookWebhookAPIView.as_view()),
]
