from django.contrib import admin

# Register Models
from .models.Page import Page
from .models.Chat import Chat
from .models.Sequence import Sequence
from .models.Template import Template

# Register to Django Admin
admin.site.register(Page)

# Register Sequence in table view
@admin.register(Sequence)
class SequenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'page']

# Register Template in table view
@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'page', 'template_name', 'template_type', 'template_content', 'sequence', 'order']

# Register Chat in table view
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'message_id',  'page', 'lead', 'message', 'timestamp']
    list_filter = ['lead']
