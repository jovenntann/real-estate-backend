from django.contrib import admin

# Models
from domain.lead.models.Lead import Lead

# Register Models
admin.site.register(Lead)
