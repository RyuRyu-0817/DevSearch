from django.apps import AppConfig


class PevsearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pevsearch'

    # def ready(self):
    #    """
    #    This function is called when startup.
    #    """
    #    from .dbUpdate import start # <= さっき作った start関数をインポート
    #    start()

