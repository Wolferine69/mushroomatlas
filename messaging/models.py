from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages_messaging', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages_messaging', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, default='No Subject')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    replied_to = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    is_deleted_by_sender = models.BooleanField(default=False)
    is_deleted_by_receiver = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"


class Attachment(models.Model):
    message = models.ForeignKey(Message, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')

    def __str__(self):
        return f"Attachment for message {self.message.id}"
