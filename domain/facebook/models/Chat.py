from django.db import models
from domain.common.models.Base import BaseModel

# Related Models
from domain.lead.models.Lead import Lead
from domain.facebook.models.Page import Page

import logging

logger = logging.getLogger(__name__)


class Chat(BaseModel):

    SENDER_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ]
        
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page_chats', null=True, blank=True)
    message_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    sender = models.CharField(
        max_length=8,
        choices=SENDER_CHOICES,
        default='admin',
    )
    page_sender = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='page_sender_chats', null=True, blank=True)
    lead_sender = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='lead_sender_chats', null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField()
    attachments = models.JSONField(null=True, blank=True)
    
    def __str__(self): # pragma: no cover
        return self.message
