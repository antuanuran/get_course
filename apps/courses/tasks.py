from celery.app import shared_task
from django.core.files.base import File

from apps.courses import service
from apps.courses.models import Certificate, Course
from apps.users.models import User


@shared_task(autoretry_for=(Exception,), max_retries=1)
def generate_certificate(course_id: int, user_id: int):
    course = Course.objects.get(id=course_id)
    user = User.objects.get(id=user_id)

    pdf_data = service.generate_certificate(course, user)

    Certificate.objects.create(course=course, user=user, pdf=File(pdf_data, name=f"{user.email}.pdf"))


@shared_task(autoretry_for=(Exception,), max_retries=2)
def send_certificate(certificate_id: int, email: str | None = None):
    cert = Certificate.objects.get(id=certificate_id)
    email = email or cert.user.email
    print(email)
