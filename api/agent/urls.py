from django.urls import path
# Views
from .leads.views import LeadsAPIView
from .messages.views import MessagesAPIView

urlpatterns = [
    path('leads', LeadsAPIView.as_view()),
    path('messages', MessagesAPIView.as_view()),
]
