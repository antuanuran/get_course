import asyncio
import time

from celery.app import shared_task

from apps.courses.models import Certificate, Course
from apps.users.models import User


@shared_task(autoretry_for=(Exception,), max_retries=1)
def generate_certificate(course_id: int, user_id: int):
    course = Course.objects.get(id=course_id)
    user = User.objects.get(id=user_id)

    cert = Certificate.objects.create(course=course, user=user, pdf="file.pdf")
    return f"Сертификат загружен! {cert.pdf}"


@shared_task(autoretry_for=(Exception,), max_retries=2)
def send_certificate(certificate_id: int, email: str | None = None):
    cert = Certificate.objects.get(id=certificate_id)
    email = email or cert.user.email
    print(email)


# Проверка asyncIO. Запуск функции происходит в Сериализаторе courses
async def fib1(value):
    time.sleep(value)
    print(value)
    return value


async def fib2(value):
    time.sleep(value)
    print(value)
    return value


async def fib3(value):
    time.sleep(value)
    print(value)
    return value


async def basic(number1, number2, number3):
    tasks = [fib1(number1), fib2(number2), fib3(number3)]
    result = await asyncio.gather(*tasks)
    print(result)
