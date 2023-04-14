import logging
import sys


def standart_logger():
    logger = logging.getLogger(name=__name__)
    logger.setLevel('DEBUG')
    handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s, %(levelname)s, %(name)s, '
        '%(funcName)s, %(levelno)s, %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
