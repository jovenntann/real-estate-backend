from django.contrib import admin

# Models
from domain.lead.models.Lead import Lead
from domain.lead.models.Status import Status
from domain.lead.models.Message import Message

# Register Models
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'company', 'status', 'facebook_id']
    list_filter = ['status']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'page', 'lead', 'source', 'sender', 'message', 'timestamp']
    list_filter = ['lead']

admin.site.register(Status)
