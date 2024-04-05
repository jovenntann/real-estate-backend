from django.urls import path
# Views
from .leads.views import LeadsAPIView

urlpatterns = [
    path('leads', LeadsAPIView.as_view()),
]
