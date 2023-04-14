import logging
import sys

from vedis import Vedis

import config

logger = logging.getLogger(name=__name__)
logger.setLevel('DEBUG')
handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s, %(levelname)s, %(name)s, '
    '%(funcName)s, %(levelno)s, %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_current_state(user_id):
    """Check current user's state"""
    with Vedis(config.db_file) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return config.States.S_START.value


def set_state(user_id, value):
    """Set current user's state"""
    with Vedis(config.db_file) as db:
        try:
            db[user_id] = value
            return True
        except Exception as e:
            logger.error(f'Ошибка записи в БД - {e}')
            return False
