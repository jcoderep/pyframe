
import os
import sys
import logging
import functools

from logging.handlers import RotatingFileHandler
from configs.user_constants import LOG_FILE


class Logger:
    """ """
    def __init__(self):
        """ """
        self._logger = None

    def config_logger(self):
        """ """
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(f'%(asctime)s - %(levelname)s - %(name)s - %(message)s')

        self.__file_handler_config(formatter, log_level=logging.DEBUG)
        self.__stream_handler_config(formatter, log_level=logging.DEBUG)

        return self._logger

    def __file_handler(self, formatter, log_level):
        """ """
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        file_handler = RotatingFileHandler(
            filename=LOG_FILE,
            mode='a',
            encoding=None,
            delay=False,
            maxBytes=1000000,
            backupCount=2
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    def __stream_handler(self, formatter, log_level):
        """ """
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(formatter)
        self._logger.addHandler(stream_handler)


class AutoMethodLogger:
    """ """
    def __init__(self, logger):
        """ """
        self.logger = logger

    def __getattribute__(self, key):
        """ """
        value = object.__getattribute__(self, key)
        if callable(value)  and not key.startswith('__'):
            log_decorator = object.__getattribute__(self, 'doc_strings_logger')
            return log_decorator
        return value

    def doc_strings_logger(self, func):
        """ """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            func_doc = func.__doc__.split('\n')[0]

            if not func_doc:
                func_doc = func.__doc__.split('\n')[1]

            if kwargs:
                self.logger.info(f"Executing {func_name}: {func_doc}, args: {kwargs}")
            else:
                self.logger.info(f"Executing {func_name}: {func_doc}")

            result = func(*args, **kwargs)
            return result
        return wrapper