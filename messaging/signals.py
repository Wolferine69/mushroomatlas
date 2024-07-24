from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from viewer.models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile instance when a new User is created.

    This function is triggered after a User instance is saved. If the User is being created
    for the first time, a corresponding Profile instance is also created.

    Args:
        sender (Model): The model class sending the signal.
        instance (User): The instance of the User being saved.
        created (bool): A boolean indicating if the User instance was created.
        **kwargs: Additional keyword arguments.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save the Profile instance when a User is saved.

    This function is triggered after a User instance is saved. It ensures that the corresponding
    Profile instance is also saved.

    Args:
        sender (Model): The model class sending the signal.
        instance (User): The instance of the User being saved.
        **kwargs: Additional keyword arguments.
    """
    instance.profile.save()
