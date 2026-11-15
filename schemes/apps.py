from django.apps import AppConfig


class SchemesConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'schemes'
