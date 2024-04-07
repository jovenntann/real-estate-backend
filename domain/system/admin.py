from django.contrib import admin

# Register Models
from .models.Company import Company
from .models.Gender import Gender

# Register to Django Admin
admin.site.register(Company)
admin.site.register(Gender)
