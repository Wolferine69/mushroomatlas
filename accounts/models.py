from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    """Model representing a user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.user.username
