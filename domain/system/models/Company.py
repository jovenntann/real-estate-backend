from django.db import models
from domain.common.models.Base import BaseModel

import logging

logger = logging.getLogger(__name__)


class Company(BaseModel):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    company_size = models.IntegerField()
    industry = models.CharField(max_length=50)

    def __str__(self): # pragma: no cover
        return self.company_name
