import csv

from django.core.management import BaseCommand

from apps.courses.models import Category, Course, Lesson, LessonTask, LessonTaskAnswer, Product


def import_data(data_stream):
    data = csv.DictReader(data_stream, delimiter=",")

    for entity in data:
        category, _ = Category.objects.get_or_create(name=entity["category"])
        product, _ = Product.objects.get_or_create(category_id=category.id, name=entity["product"])
        course, _ = Course.objects.get_or_create(
            author_id=entity["author"], name=entity["course"], product_id=product.id, price=entity["price"]
        )
        lesson, _ = Lesson.objects.get_or_create(course_id=course.id, name=entity["lesson"])
        lesson_task, _ = LessonTask.objects.get_or_create(
            lesson_id=lesson.id, title=entity["LessonTask"], auto_test=True
        )
        lessontaskanswer, _ = LessonTaskAnswer.objects.get_or_create(task_id=lesson_task.id, text=entity["answer"])

        # image, _ = ImageHolder.objects.get_or_create(name="Photo_1", file="files/images/foto1.png")
        # image, _ = VideoHolder.objects.get_or_create(name="Video_1", file="files/videos/video_1.mp4")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path")

    def handle(self, path, *args, **options):
        with open(path, "r") as file:
            import_data(file)


# python manage.py import_data data_all/import.csv
