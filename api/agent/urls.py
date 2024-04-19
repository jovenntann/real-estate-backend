from django.urls import path
# Views
from .leads.views import LeadsAPIView
from .leads.id.views import LeadIdAPIView
from .leads.id.messages.views import LeadsIdMessagesAPIView
from .leads.messages.views import LeadsMessagesAPIView
from .messages.views import MessagesAPIView
from .system.company.views import AgentSystemCompanyAPIView


urlpatterns = [
    path('leads', LeadsAPIView.as_view()),
    path('leads/<int:lead_id>', LeadIdAPIView.as_view()),
    path('leads/<int:lead_id>/messages', LeadsIdMessagesAPIView.as_view()),
    path('leads/messages', LeadsMessagesAPIView.as_view()),
    path('messages', MessagesAPIView.as_view()),
    path('system/company', AgentSystemCompanyAPIView.as_view()),
]
