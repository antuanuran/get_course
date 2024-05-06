from django.apps import AppConfig

from .scrapping_beautiful import main


class BeautifulSoupConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.beautiful_soup"

    def ready(self):
        main()
