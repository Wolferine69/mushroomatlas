from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Message, Attachment


class AttachmentInline(admin.TabularInline):
    model = Attachment


class MessageAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline]
    list_display = ('subject', 'sender', 'receiver', 'timestamp', 'is_read')
    search_fields = ('subject', 'content', 'sender__username', 'receiver__username')


admin.site.register(Message, MessageAdmin)
admin.site.register(Attachment)
