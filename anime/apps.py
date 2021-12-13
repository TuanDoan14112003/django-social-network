from django.apps import AppConfig


class AnimeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'anime'
    def ready(self):
        import anime.signals
