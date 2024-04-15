from django.db import models
from domain.common.models.Base import BaseModel
from domain.facebook.models.Page import Page

import logging
logger = logging.getLogger(__name__)


class Sequence(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='sequences')

    def __str__(self): # pragma: no cover
        return self.name
