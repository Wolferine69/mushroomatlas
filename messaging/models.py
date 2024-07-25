from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    """
    Model representing a message.

    Attributes:
        sender (ForeignKey): The user who sent the message.
        receiver (ForeignKey): The user who received the message.
        subject (CharField): The subject of the message.
        content (TextField): The content of the message.
        timestamp (DateTimeField): The time when the message was sent.
        replied_to (ForeignKey): The message to which this message is a reply.
        is_read (BooleanField): Whether the message has been read.
        is_deleted_by_sender (BooleanField): Whether the message is deleted by the sender.
        is_deleted_by_receiver (BooleanField): Whether the message is deleted by the receiver.
        is_trashed_by_sender (BooleanField): Whether the message is trashed by the sender.
        is_trashed_by_receiver (BooleanField): Whether the message is trashed by the receiver.
    """
    sender = models.ForeignKey(User, related_name='sent_messages_messaging', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages_messaging', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, default='No Subject')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    replied_to = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    is_deleted_by_sender = models.BooleanField(default=False)
    is_deleted_by_receiver = models.BooleanField(default=False)
    is_trashed_by_sender = models.BooleanField(default=False)
    is_trashed_by_receiver = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"


class Attachment(models.Model):
    """
    Model representing an attachment.

    Attributes:
        message (ForeignKey): The message to which the attachment belongs.
        file (FileField): The file attached to the message.
    """
    message = models.ForeignKey(Message, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')

    def __str__(self):
        return f"Attachment for message {self.message.id}"

    def delete(self, *args, **kwargs):
        """
        Deletes the file associated with the attachment before deleting the model instance.
        """
        self.file.delete(save=False)
        super().delete(*args, **kwargs)
