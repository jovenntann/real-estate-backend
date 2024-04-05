from django.db import models
from domain.common.models.Base import BaseModel

import logging

logger = logging.getLogger(__name__)


class LeadStatus(BaseModel):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50, unique=True)

    def __str__(self): # pragma: no cover
        return self.status

    class Meta:
        verbose_name = "Lead Status"
        verbose_name_plural = "Lead Statuses"