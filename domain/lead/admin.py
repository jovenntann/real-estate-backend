from django.contrib import admin

# Models
from domain.lead.models.Lead import Lead
from domain.lead.models.Status import Status
from domain.lead.models.Message import Message
from domain.lead.models.MessageStatus import MessageStatus

# Register Models
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'company', 'status', 'facebook_id', 'last_message_at']
    list_filter = ['status']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'page', 'lead', 'source', 'sender', 'message', 'timestamp']
    list_filter = ['lead']

@admin.register(MessageStatus)
class MessageStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'description']
    list_filter = ['status']

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'color']
