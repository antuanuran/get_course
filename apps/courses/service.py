import datetime
import io
import os

import weasyprint
from django.http import HttpRequest
from django.template import RequestContext, Template

from apps.courses.models import Course
from apps.users.models import User

CURRENT_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(CURRENT_DIR, "templates")


def generate_certificate(course: Course, user: User) -> bytes | bytearray | io.BytesIO:
    # render template
    with open(os.path.join(TEMPLATE_DIR, "certificate.html"), "r") as fd:
        template = Template(fd.read())
    context = RequestContext(
        HttpRequest(),
        {"user_name": user.get_full_name() or user.email, "course_name": course.name, "date": datetime.date.today()},
    )
    html_out = template.render(context)
    html = weasyprint.HTML(string=html_out)

    # convert it to bytestream
    bstream = io.BytesIO()
    html.write_pdf(bstream)
    bstream.seek(0)
    return bstream


def generate_report():
    with open(os.path.join(TEMPLATE_DIR, "report.html"), "r") as fd:
        template = Template(fd.read())
    context = RequestContext(
        HttpRequest(),
        {"date": datetime.date.today()},
    )
    html_out = template.render(context)
    html = weasyprint.HTML(string=html_out)

    # convert it to bytestream
    bstream = io.BytesIO()
    html.write_pdf(bstream)
    bstream.seek(0)
    return bstream
