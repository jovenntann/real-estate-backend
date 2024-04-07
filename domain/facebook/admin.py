from django.contrib import admin

# Register Models
from .models.Page import Page
from .models.Chat import Chat

# Register to Django Admin
admin.site.register(Page)
admin.site.register(Chat)
