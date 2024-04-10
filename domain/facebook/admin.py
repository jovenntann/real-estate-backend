from django.contrib import admin

# Register Models
from .models.Page import Page
from .models.Chat import Chat

# Register to Django Admin
admin.site.register(Page)

# Register Chat in table view
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'message_id',  'page', 'lead', 'message', 'timestamp']
    list_filter = ['lead']
