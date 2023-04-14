import asyncio
import datetime
import os
import sys
import time

import aiogram
from dotenv import load_dotenv

import config
import db_worker
import keyboards
from exceptions import DateTimeError, TokenNotFoundError
from homework_status import check_response, get_api_answer, parse_status
from loggers import standart_logger

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')

logger = standart_logger()
bot = aiogram.Bot(token=TELEGRAM_TOKEN)
dp = aiogram.Dispatcher(bot)


def check_tokens() -> bool:
    """Token exist check."""
    tokens = {
        'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN
    }
    no_value = [
        token_name for token_name,
        token_value in tokens.items() if not token_value
    ]
    if no_value:
        logger.critical(
            TokenNotFoundError(no_value)
        )
        return False
    logger.info('Переменные окружения доступны.')
    return True


def make_time(date: str) -> int:
    """Make datetime object form user's message"""
    try:
        maked = datetime.datetime.strptime(date, '%d.%m.%Y')
        maked = time.mktime(maked.timetuple())
        return int(maked)
    except Exception as e:
        logger.error(DateTimeError(e))
        return False


def get_homework_status(timestamp):
    """Get homework status"""
    current_time = timestamp
    response = get_api_answer(current_time)
    homework = check_response(response)
    status = parse_status(homework)
    return status


@dp.message_handler(commands=['start'])
async def cmd_start(message: aiogram.types.Message):
    await message.reply(
        'Я здесь и готов служить!'
        'Проверить статус ДЗ?',
        reply_markup=keyboards.kb1
    )


@dp.message_handler(aiogram.filters.Text(equals='Проверить'))
async def check(message: aiogram.types.Message):
    chat_id = message.chat.id
    current_time = int(time.time())
    await bot.send_message(
        chat_id=chat_id,
        text=get_homework_status(current_time)
    )
    db_worker.set_state(chat_id, config.States.S_START.value)


@dp.message_handler(aiogram.filters.Text(equals='Проверить с даты'))
async def check_from_date(message: aiogram.types.Message):
    chat_id = message.chat.id
    await bot.send_message(
        chat_id=chat_id,
        text='Введите дату в формате DD.MM.YYYY'
    )
    db_worker.set_state(chat_id, config.States.S_ENTER_DATE.value)


@dp.message_handler(
    lambda message: db_worker.get_current_state(
        message.chat.id) == config.States.S_ENTER_DATE.value
)
async def entering_date(message: aiogram.types.Message):
    chat_id = message.chat.id
    logger.debug(type(message.text))
    if not make_time(message.text):
        await bot.send_message(
            chat_id=chat_id,
            text='Неверный формат даты, введите дату в формате DD.MM.YYYY'
        )
        return
    await bot.send_message(
        chat_id=chat_id,
        text=get_homework_status(make_time(message.text))
    )
    db_worker.set_state(config.States.S_START.value)


@dp.message_handler(aiogram.filters.Text(equals='Отмена'))
async def cancel_from_date(message: aiogram.types.Message):
    chat_id = message.chat.id
    await bot.send_message(
        chat_id=chat_id,
        text='Отменено'
    )
    db_worker.set_state(chat_id, config.States.S_START.value)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    if check_tokens():
        asyncio.run(main())
    sys.exit(
        'Отсутствуют необходимые переменные окружения. '
        'Программа будет остановлена.'
    )
