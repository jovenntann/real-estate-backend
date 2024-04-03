from django.contrib import admin

# Register Models
from .models.CompanyInformation import CompanyInformation
from .models.Gender import Gender

# Register to Django Admin
admin.site.register(CompanyInformation)
admin.site.register(Gender)
