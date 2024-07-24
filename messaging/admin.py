from django.contrib import admin
from .models import Message, Attachment


class AttachmentInline(admin.TabularInline):
    """
    Inline admin interface for Attachment model.

    This allows attachments to be edited directly within the Message admin interface.
    """
    model = Attachment


class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface for the Message model.

    This defines how the Message model is displayed and managed in the admin interface.

    Attributes:
        inlines (list): List of inline models to display within the Message admin interface.
        list_display (tuple): Fields to display in the list view.
        search_fields (tuple): Fields to include in the search functionality.
    """
    inlines = [AttachmentInline]
    list_display = ('subject', 'sender', 'receiver', 'timestamp', 'is_read')
    search_fields = ('subject', 'content', 'sender__username', 'receiver__username')


# Register the models with the admin site
admin.site.register(Message, MessageAdmin)
admin.site.register(Attachment)
