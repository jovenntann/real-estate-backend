from django.db import models
from domain.common.models.Base import BaseModel

import logging
logger = logging.getLogger(__name__)


class Page(BaseModel):
    id = models.AutoField(primary_key=True)
    page_name = models.CharField(max_length=50, unique=True)
    page_id = models.CharField(max_length=50, unique=True)
    access_token = models.CharField(max_length=255)

    def __str__(self): # pragma: no cover
        return self.page_name
