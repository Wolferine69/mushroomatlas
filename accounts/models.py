from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Model representing a user's profile.

    Attributes:
        user (OneToOneField): A one-to-one relationship to the User model.
        biography (TextField): A field for the user's biography, optional.
        profile_picture (ImageField): A field for the user's profile picture, optional.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    class Meta:
        """
        Meta options for the Profile model.

        Attributes:
            ordering (list): Default ordering for Profile objects.
        """
        ordering = ['user__username']

    def __str__(self):
        """
        String representation of the Profile model.

        Returns:
            str: The username of the associated User.
        """
        return self.user.username
