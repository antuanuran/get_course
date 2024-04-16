import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, F, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("TOKEN_AIOGRAM")

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

database = {}


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}! Введи свою почту, чтобы я нашел тебя в <b>skillsup</b>"
    )


@dp.message(F.text, Command("antuanuran"))
async def any_message(message: Message):
    await message.answer(f"Я уже понял, что ты {html.bold(message.from_user.full_name)}! Вводи уже почту!")


@dp.message(F.text)
async def get_email(message: Message) -> None:
    if message.text in database:
        answer = "уже все хорошо, я тебя помню, буду присылать уведомления"
    elif "@" in message.text:
        database[message.text] = message.chat.id
        answer = "все хорошо, буду присылать уведомления"
    else:
        answer = "фигня какая-то, попробуй еще раз отправить email"
    await message.answer(answer)


@dp.message()
async def echo_handler(message: Message) -> None:
    await message.answer("фигня какая-то, попробуй еще раз отправить email")


async def test():
    print("Start")
    await asyncio.sleep(15)
    print("GO")
    email = "hi@hi"
    chat_id = database.get(email)
    if chat_id is not None:
        await bot.send_message(chat_id, f"открылся новый урок, ваш чат id = {chat_id}")


async def main() -> None:
    await asyncio.gather(test(), dp.start_polling(bot))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

# t.me/antuanuran_bot
