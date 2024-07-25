from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration for the Accounts application.

    This class defines the configuration settings for the 'accounts' app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    """
    Attributes:
        default_auto_field (str): Specifies the type of field to use for auto-generated primary keys.
        name (str): The name of the application.
    """
