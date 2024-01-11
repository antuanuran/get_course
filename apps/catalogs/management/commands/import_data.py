import os.path
from apps.catalogs.service import import_data

from django.core.management import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path")
        parser.add_argument("--owner_id")

    def handle(self, path, *args, **options):
        data_format = os.path.splitext(os.path.basename(path))[-1][1:]

        with open(path, "r") as file:
            import_data(file, data_format, options["owner_id"])


# python3 manage.py import_data data_all/import.csv --owner_id 1
