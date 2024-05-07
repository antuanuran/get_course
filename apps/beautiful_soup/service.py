import datetime
import io
import os

import weasyprint
from django.http import HttpRequest
from django.template import RequestContext, Template

CURRENT_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(CURRENT_DIR, "templates")


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
