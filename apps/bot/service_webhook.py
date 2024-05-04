from contextlib import suppress

import requests
from django.conf import settings

from apps.bot.models import TgUser
from apps.purchases.models import Purchase
from apps.users.models import User


# start
def command_start_handler(tg_user_id, name, message):
    with suppress(Exception):
        requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": tg_user_id, "text": f" Привет, {name}, Введи свою почту, чтобы я нашел тебя в базе"},
        )


def answer(tg_user_id):
    with suppress(Exception):
        requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": tg_user_id, "text": "я вас не знаю, выполните /start "},
        )


def get_email(tg_user_id, message, user_name):
    tg_user = TgUser.objects.filter(user__email=message, id=tg_user_id).first()
    if tg_user:
        answer = "уже все хорошо, я тебя помню, буду присылать уведомления"

    else:
        user = User.objects.filter(email=message).first()
        if user:
            try:
                tg_user, _ = TgUser.objects.get_or_create(
                    user=user,
                    id=tg_user_id,
                    username=user_name,
                )
                answer = "все хорошо, буду присылать уведомления"

            except:  # noqa: E722
                answer = "что-то пошло не так, попробуйте позднее"
        else:
            answer = "либо ошибся в email, либо еще не зарегистрирован в нашей системе"

    with suppress(Exception):
        requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": tg_user_id, "text": f" {answer} "},
        )


def all_purchases(chat_id):
    tg_user = TgUser.objects.filter(id=chat_id).first()

    for purchase in Purchase.objects.filter(user_id=tg_user.user.id).all():
        requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": f" {purchase} "},
        )


def notify_about_new_lesson(user_ids: list[int], lesson_title: str, course):
    for tg_user_id in TgUser.objects.filter(user_id__in=user_ids).values_list("id", flat=True):
        with suppress(Exception):
            requests.post(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": tg_user_id, "text": f' Урок: "{lesson_title}" по курсу: {course}'},
            )


def pay_purchases(user_email, course: str):
    tg_user_id = TgUser.objects.get(user__email=user_email).id
    with suppress(Exception):
        requests.post(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": tg_user_id, "text": f'Вы только что приобрели новый курс: "{course}"'},
        )


#
#
