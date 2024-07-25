from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Model representing a user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    class Meta:
        ordering = ['user__username']
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_user_profile')]

    def __str__(self):
        return self.user.username