from django.db import models
from domain.common.models.Base import BaseModel

# Related Models
from domain.lead.models.Lead import Lead
from domain.facebook.models.Page import Page

import logging

logger = logging.getLogger(__name__)


class Message(BaseModel):
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='messages')
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='messages')
    source = models.CharField(max_length=20, choices=[('messenger', 'Messenger'), ('sms', 'SMS'), ('call', 'Call')], default='messenger')
    sender = models.CharField(max_length=10, choices=[('customer', 'Customer'), ('admin', 'Admin')], default='admin')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # SMS Platform
    # twilio models.ForeignKey(Twilio, on_delete=models.CASCADE, related_name='messages')

    def __str__(self): # pragma: no cover
        return f"Message {self.id} for Lead {self.lead.id} from {self.source}"
