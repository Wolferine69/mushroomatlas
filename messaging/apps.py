from django.apps import AppConfig


class MessagingConfig(AppConfig):
    """
    Configuration for the Messaging application.

    This class defines the configuration settings for the 'messaging' app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

    def ready(self):
        """
        Import signals when the app is ready.

        This method is called when the application is ready for use. It ensures that
        the signal handlers are imported and registered.
        """
        import messaging.signals
