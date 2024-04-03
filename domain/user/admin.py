from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import User


# Register to Django Admin
class CustomUserAdmin(UserAdmin):
    fieldsets = list(UserAdmin.fieldsets)
    fieldsets[1] = (None, {'fields': ('first_name', 'last_name', 'middle_name', 'email')})

admin.site.register(User, CustomUserAdmin)