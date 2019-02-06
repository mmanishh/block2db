# coding=utf-8
import logging
from logging import StreamHandler

import sys


class Logger:

    def __init__(self):
        logging.basicConfig(filename='debug.log', filemode='w',
                                           format='%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — '
                                                  '%(message)s',level=logging.INFO)
        stream_handler = StreamHandler(sys.stdout)

        self.logger = logging.getLogger()
        self.logger.addHandler(stream_handler)

    @staticmethod
    def warning(msg):
        logging.warning(msg)

    @staticmethod
    def debug(msg):
        logging.debug(msg)

    @staticmethod
    def error(msg):
        logging.error(msg)

    @staticmethod
    def critical(msg):
        logging.critical(msg)

    @staticmethod
    def info(msg):
        logging.info(msg)
