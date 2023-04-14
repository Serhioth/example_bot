import logging
import os
import sys
from http import HTTPStatus

import requests
from dotenv import load_dotenv

from exceptions import ResponseError, ResponseStatusError

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')

ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(name=__name__)
logger.setLevel('DEBUG')
handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(name)s, '
    '%(funcName)s, %(levelno)s, %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_api_answer(timestamp):
    """Getting response from the API."""
    payload = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload)
        if response.status_code != HTTPStatus.OK:
            logger.error(
                f'Ошибка при обращении к серверу {response.status_code}.'
            )
            raise ResponseStatusError(
                f'Ошибка при обращении к серверу {response.status_code}.'
            )
    except requests.RequestException as error:
        logger.error(
            f'API вернул ошибку - {error}.'
        )
        raise ResponseError(
            f'API вернул ошибку - {error}.'
        )
    return response.json()


def check_response(response):
    """Response status check."""
    if not isinstance(response, dict):
        logger.error(
            f'Неверный тип данных в ответе от сервера - {type(response)}.'
        )
        raise TypeError(
            f'Неверный тип данных в ответе от сервера - {type(response)}.'
        )
    elif 'homeworks' not in response:
        logger.error(
            'Ключ homeworks отсутствует в response. '
            f'Доступные ключи: {response.keys()}.'
        )
        raise KeyError(
            'Ключ homeworks отсутствует в response. '
            f'Доступные ключи: {response.keys()}.'
        )

    homework = response.get('homeworks')
    logger.debug(homework)

    if not isinstance(homework, list):
        logger.error(
            f'Неверный тип данных по ключу homeworks - {type(homework)}.'
        )
        raise TypeError(
            f'Неверный тип данных по ключу homeworks - {type(homework)}.'
        )
    elif not homework:
        logger.debug(
            'Статус домашней работы не обновлён,'
            'или нет работ в заданном интервале.'
        )
        homework = False
        return homework
    return homework[0]


def parse_status(homework):
    """Parsing status of the homework."""
    if homework:
        logger.debug(homework)
        keys = ['homework_name', 'status']
        for key in keys:
            if key not in homework:
                logger.error(
                    'В ответе от сервера отсутствуют '
                    f'необходимые данные - {key}.'
                )
                raise KeyError(
                    'В ответе от сервера отсутствуют '
                    f'необходимые данные - {key}. '
                    f'Доступные ключи - {homework.keys()}'
                )
        homework_status = homework.get('status')
        if homework_status not in HOMEWORK_VERDICTS:
            logger.error(
                f'Неизвестный статус {homework_status} домашней работы.'
            )
            raise KeyError(
                f'Неизвестный статус {homework_status} домашней работы.'
            )
        homework_name = homework.get('homework_name')
        verdict = HOMEWORK_VERDICTS.get(homework_status)
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'
    return '''Статус домашней работы не обновлён,
или нет работ в заданном интервале.'''
