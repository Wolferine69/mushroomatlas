from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Configuration for the API application.

    This class defines the configuration settings for the 'api' app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    """
    Attributes:
        default_auto_field (str): Specifies the type of field to use for auto-generated primary keys.
        name (str): The name of the application.
    """
