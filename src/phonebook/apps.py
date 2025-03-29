from django.apps import AppConfig


class PhonebookConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "phonebook"

    def ready(self):
        import phonebook.signals  # noqa: F403, F401
