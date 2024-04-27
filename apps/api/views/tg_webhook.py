from asgiref.sync import AsyncToSync
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.bot.service import bot, dp

sync_update = AsyncToSync(dp.feed_raw_update)


@api_view(http_method_names=["post"])
@permission_classes([AllowAny])
def tg_callback(request, token, *args, **kwargs):
    if token != settings.TELEGRAM_WEBHOOK_TOKEN:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        sync_update(bot(), request.data)
        # await dp.feed_raw_update(bot(), request.data)
    except Exception as e:
        print(e)

    return Response({"success": True})
