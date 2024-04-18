from django.db import models
from domain.common.models.Base import BaseModel

import logging

logger = logging.getLogger(__name__)


class NextAction(BaseModel):
    id = models.AutoField(primary_key=True)
    action = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=50, default="default")
    
    def __str__(self): # pragma: no cover
        return self.action

    class Meta:
        verbose_name = "Next Action"
        verbose_name_plural = "Next Actions"
