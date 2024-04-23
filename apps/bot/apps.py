from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.bot"

    def ready(self):
        from apps.bot.service import bot

        bot.delete_webhook()
        bot.set_webhook(url="https://skillsup.fun/api/v1/tg-updates")
