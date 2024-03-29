import logging

from celery.app import shared_task
from django.conf import settings
from django.core.files.base import File
from django.core.mail import send_mail

from apps.courses import service
from apps.courses.models import Certificate, Course
from apps.users.models import User

logger = logging.getLogger(__name__)


@shared_task(autoretry_for=(Exception,), max_retries=1)
def generate_certificate(course_id: int, user_id: int):
    logger.info(f"Generate certificate {course_id=}, {user_id=}")
    course = Course.objects.get(id=course_id)
    user = User.objects.get(id=user_id)

    pdf_data = service.generate_certificate(course, user)

    Certificate.objects.create(course=course, user=user, pdf=File(pdf_data, name=f"{user.email}.pdf"))
    logger.info(f"Generate certificate has been completed {course_id=}, {user_id=}")


@shared_task(autoretry_for=(Exception,), max_retries=2)
def send_certificate(certificate_id: int, email: str | None = None):
    logger.info(f"Send certificate via email {certificate_id=}, {email=}")
    cert = Certificate.objects.get(id=certificate_id)
    email = email or cert.user.email

    send_mail(
        subject=f"Ваш сертификат о прохождении курса: {cert.course.name}",
        message=f"Ссылка на сертификат: {cert.full_url}",
        from_email=settings.CERTIFICATE_EMAIL_FROM,
        recipient_list=[email],
        html_message=f"<h1>Поздравляем!</h1><p>Ссылка на сертификат: {cert.full_url}</p>",
        fail_silently=False,
    )
    logger.info(f"Certificate has been sent {certificate_id=}, {email=}")


@shared_task(autoretry_for=(Exception,), max_retries=2, default_retry_delay=5)
def generate_and_send_email(course_id: int, user_id: int):
    cert = Certificate.objects.filter(course_id=course_id, user_id=user_id).first()
    if not cert:
        generate_certificate(course_id, user_id)
        cert = Certificate.objects.filter(course_id=course_id, user_id=user_id).first()
    print("здесь происходит отправка на email.. -> send_certificate(cert.id)")
    # send_certificate(cert.id)
