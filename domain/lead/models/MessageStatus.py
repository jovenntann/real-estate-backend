from django.db import models
from domain.common.models.Base import BaseModel

# Model
from domain.system.models.Company import Company

import logging
logger = logging.getLogger(__name__)


class MessageStatus(BaseModel):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='lead_message_statuses', default=1)
    status = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self): # pragma: no cover
        return f"{self.status}"

    class Meta:
        verbose_name = "Message Status"
        verbose_name_plural = "Message Statuses"