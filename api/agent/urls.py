from django.urls import path
# Views
from .leads.views import LeadsAPIView
from .leads.id.messages.views import LeadsIdMessagesAPIView
from .messages.views import MessagesAPIView

urlpatterns = [
    path('leads', LeadsAPIView.as_view()),
    path('leads/<int:lead_id>/messages', LeadsIdMessagesAPIView.as_view()),
    path('messages', MessagesAPIView.as_view()),
]
