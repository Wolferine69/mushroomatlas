from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    """Model representing a user."""
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)


    def __str__(self):
        return self.username
