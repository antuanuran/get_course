import csv

from django.core.management import BaseCommand

from apps.courses.models import Category, Course, Lesson, LessonTask, LessonTaskAnswer, Link, Product


def import_data(data_stream):
    data = csv.DictReader(data_stream, delimiter=",")

    for entity in data:
        category, _ = Category.objects.get_or_create(name=entity["category"])
        product, _ = Product.objects.get_or_create(category_id=category.id, name=entity["product"])
        course, _ = Course.objects.get_or_create(
            author_id=entity["author"], name=entity["course"], product_id=product.id, price=entity["price"]
        )
        lesson, _ = Lesson.objects.get_or_create(course_id=course.id, name=entity["lesson"])
        link, _ = Link.objects.get_or_create(lesson_id=lesson.id, link="https://quote.rbc.ru/ticker/59111")
        lesson_task, _ = LessonTask.objects.get_or_create(
            lesson_id=lesson.id, title="1 Задание по Маркетингу", auto_test=True
        )
        lessontaskanswer, _ = LessonTaskAnswer.objects.get_or_create(
            task_id=lesson_task.id, text="Ответ на Задание", is_correct=True
        )


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path")

    def handle(self, path, *args, **options):
        with open(path, "r") as file:
            import_data(file)


# python manage.py import_data data_all/import.csv
