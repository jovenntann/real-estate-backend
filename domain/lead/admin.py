from django.contrib import admin

# Models
from domain.lead.models.Lead import Lead
from domain.lead.models.Status import Status
from domain.lead.models.Message import Message

# Register Models
admin.site.register(Lead)
admin.site.register(Status)
admin.site.register(Message)
