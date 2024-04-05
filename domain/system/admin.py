from django.contrib import admin

# Register Models
from .models.Company import Company
from .models.Gender import Gender
from .models.LeadStatus import LeadStatus

# Register to Django Admin
admin.site.register(Company)
admin.site.register(Gender)
admin.site.register(LeadStatus)
