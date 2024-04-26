from django.apps import AppConfig


class BotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.bot"

    def ready(self):
        from django.conf import settings

        if settings.TELEGRAM_WEBHOOK_CALLBACK:
            import asyncio

            from apps.bot import service

            async def start_webhook():
                await service.bot().delete_webhook()
                await service.bot().set_webhook(url=settings.TELEGRAM_WEBHOOK_CALLBACK)

            asyncio.run(start_webhook())
