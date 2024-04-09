from django.contrib import admin

# Register Models
from .models.Page import Page
from .models.Chat import Chat

# Register to Django Admin
admin.site.register(Page)

# Register Chat in table view
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'page', 'message_id', 'sender', 'page_sender', 'lead_sender', 'message', 'timestamp']