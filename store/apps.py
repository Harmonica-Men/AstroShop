from django.apps import AppConfig


class StoreConfig(AppConfig):
    """
    Configuration class for the 'store' app.

    This class sets the default primary key field type
    and the application name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
