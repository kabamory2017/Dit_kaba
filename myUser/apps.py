from django.apps import AppConfig


class MyuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myUser'
    def ready(self):
        import myUser.signals
