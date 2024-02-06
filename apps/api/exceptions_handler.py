import traceback

from django.conf import settings
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return response

    data = {"message": str(exc)}
    if settings.DEBUG:
        data["trace"] = traceback.format_exc().split("\n")
    unexpected_exc = APIException(data)
    unexpected_exc.__cause__ = exc
    return exception_handler(unexpected_exc, context)
