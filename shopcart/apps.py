from django.apps import AppConfig


class ShopcartConfig(AppConfig):
    """
    Configuration for the 'shopcart' application in the Django project.

    This class sets the default auto field type for the application to 
    BigAutoField, which automatically generates a large integer for model 
    primary keys. It also specifies the name of the app, 'shopcart', which 
    Django uses to identify the app in the project settings.

    Attributes:
        default_auto_field (str): The type of field to use for automatically 
                                   generated primary keys. Default is 
                                   'BigAutoField'.
        name (str): The name of the application, used by Django for app 
                    identification.
    """
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopcart'
