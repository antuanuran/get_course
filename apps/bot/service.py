from contextlib import suppress

from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

# from aiogram.filters import Command
from aiogram.types import Message
from django.conf import settings

from apps.bot.models import TgUser
from apps.users.models import User

dp = Dispatcher()
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}! Введи свою почту, чтобы я нашел тебя в <b>skillsup</b>"
    )


# @dp.message(F.text, Command("antuanuran"))
# async def any_message(message: Message):
#     await message.answer(f"Я уже понял, что ты {html.bold(message.from_user.full_name)}! Вводи уже почту!")


@dp.message(F.text)
async def get_email(message: Message) -> None:
    email = message.text
    tg_user = await TgUser.objects.filter(user__email=email, id=message.from_user.id).afirst()
    if tg_user:
        answer = "уже все хорошо, я тебя помню, буду присылать уведомления"

    else:
        user = await User.objects.filter(email=email).afirst()
        if user:
            try:
                await TgUser.objects.acreate(
                    user=user,
                    id=message.from_user.id,
                    username=message.from_user.username,
                    extra_data=message.from_user.model_dump(exclude={"username"}),
                )
                answer = "все хорошо, буду присылать уведомления"
            except:  # noqa: E722
                answer = "что-то пошло не так, попробуйте позднее"
        else:
            answer = "либо ошибся в email, либо еще не зарегистрирован в нашей системе"
    await message.answer(answer)


async def notify_about_new_lesson(user_ids: list[int], lesson_title: str):
    async for tg_user_id in TgUser.objects.filter(user_id__in=user_ids).values_list("id", flat=True):
        with suppress(Exception):
            await bot.send_message(tg_user_id, f"открылся новый урок '{lesson_title}'")


async def main() -> None:
    await dp.start_polling(bot)
