from django.contrib import admin

from .models import WhatsAppDocument

# Register your models here.
@admin.register(WhatsAppDocument)
class WhatsAppDocumentAdmin(admin.ModelAdmin):
    list_display = ('sender_number', 'uploaded_at', 'image')
