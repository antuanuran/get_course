from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.bot.service_webhook import all_purchases, command_start_handler, get_email


@api_view(http_method_names=["post"])
@permission_classes([AllowAny])
def tg_callback(request, token, *args, **kwargs):
    if token != settings.TELEGRAM_WEBHOOK_TOKEN:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        all = request.data
        chat_id = all["message"]["chat"]["id"]
        first_name = all["message"]["chat"]["first_name"]
        message = all["message"]["text"]

        if message == "/start":
            command_start_handler(chat_id, first_name, message)

        elif message == "/pay":
            all_purchases(chat_id)

        else:
            get_email(chat_id, message, first_name)

    except Exception as e:
        print(e)

    return Response({"success": True})
