from django.db import models
from domain.common.models.Base import BaseModel

# Models
from domain.system.models.Company import Company

import logging
logger = logging.getLogger(__name__)


class Status(BaseModel):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='lead_statuses', default=1)
    status = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=50, default="default")
    
    def __str__(self): # pragma: no cover
        return self.status

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"