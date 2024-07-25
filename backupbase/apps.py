from django.apps import AppConfig


class BackupbaseConfig(AppConfig):
    """
    Configuration for the Backupbase application.

    This class defines the configuration settings for the 'backupbase' app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backupbase'
    """
    Attributes:
        default_auto_field (str): Specifies the type of field to use for auto-generated primary keys.
        name (str): The name of the application.
    """
