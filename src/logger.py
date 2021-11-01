import os
import logging
from logging.handlers import RotatingFileHandler
import colorlog

def init_logger(name, debug_mode=False):
    color_log_format = (
        '%(asctime)s '
        '%(log_color)s'
        '%(levelname)s '
        '%(reset)s'
        '%(message)s '
        '- %(processName)s %(threadName)s '
        '- %(filename)s:%(funcName)s:%(lineno)d'
        '%(reset)s'
    )
    log_format = (
        '%(asctime)s '
        '%(levelname)s - '
        '%(message)s '
        '%(filename)s:%(funcName)s;%(lineno)d'
    )
    colorlog.basicConfig(format=color_log_format)
    logger = logging.getLogger(name)

    if debug_mode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Output full log
    logging_dir = 'logs'
    if not os.path.exists(logging_dir):
        os.makedirs(logging_dir)

    handler = RotatingFileHandler(f'{logging_dir}/%s.log' % name,
                             mode='a',
                             maxBytes=5*1024*1024,
                             backupCount=3)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Output warning log
    handler = RotatingFileHandler(f'{logging_dir}/%s.warn.log' % name,
                             mode='a',
                             maxBytes=5*1024*1024,
                             backupCount=3)
    handler.setLevel(logging.WARNING)
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Output error log
    handler = RotatingFileHandler(f'{logging_dir}/%s.err.log' % name,
                             mode='a',
                             maxBytes=5*1024*1024,
                             backupCount=3)
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger