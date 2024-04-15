from django.db import models
from domain.common.models.Base import BaseModel

# Related Models
from .Sequence import Sequence
from .Page import Page

import logging
logger = logging.getLogger(__name__)


class Template(BaseModel):
    id = models.AutoField(primary_key=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='templates')
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE, related_name='templates')
    template_name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=100)
    template_content = models.JSONField()
    delay = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField()

    def __str__(self): # pragma: no cover
        return self.template_type
