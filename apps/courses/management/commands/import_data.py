import csv

from django.core.management import BaseCommand

from apps.courses.models import Category, Course, Lesson, Product


def import_data(data_stream):
    data = csv.DictReader(data_stream, delimiter=",")

    for entity in data:
        category, _ = Category.objects.get_or_create(name=entity["category"])
        product, _ = Product.objects.get_or_create(category_id=category.id, name=entity["product"])
        course, _ = Course.objects.get_or_create(
            author_id=entity["author"], name=entity["course"], product_id=product.id, price=entity["price"]
        )
        lesson, _ = Lesson.objects.get_or_create(course_id=course.id, name=entity["lesson"])


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path")

    def handle(self, path, *args, **options):
        with open(path, "r") as file:
            import_data(file)


# python3 manage.py import_data data_all/import.csv
