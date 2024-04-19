import asyncio
import logging
import sys

from django.core.management import BaseCommand

from apps.bot.service import main


class Command(BaseCommand):
    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
