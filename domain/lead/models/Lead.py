from django.db import models
from domain.common.models.Base import BaseModel

# Related Models
from domain.system.models.Company import Company
from .Status import Status

import logging

logger = logging.getLogger(__name__)


class Lead(BaseModel):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='leads')
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    facebook_id = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self): # pragma: no cover
        return f"{self.first_name} {self.last_name}"