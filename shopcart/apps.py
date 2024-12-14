from django.apps import AppConfig


class ShopcartConfig(AppConfig):
    """
    Configuration for the 'shopcart' app in the Django project.
    Sets the default primary key type to
    'BigAutoField' and specifies the app name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopcart'
