from logging import (
    Filter       ,
    Formatter    ,
    StreamHandler,
    addLevelName ,
    getLevelName ,
    getLogger    ,
)
from bot_commands.bot_utils import delay
from random import randint
from sys    import stdout
from time   import sleep

class BotLogger:
    STATUS = 9001
    while 'Level' not in getLevelName(STATUS):
        STATUS = randint(100, 10000)
    def __init__(self, fmt, level=20):
        self.logger = getLogger(__name__)

        self.verbosity_translator = {
            1: 40, # ERROR
            2: 30, # WARNING
            3: 20, # INFO
            4: 10, # DEBUG
        }

        self.initialize_logger(level, fmt)

        def status(message, *args, **kwargs):
            self.logger.log(BotLogger.STATUS, message, *args, **kwargs)
        self.logger.status = status

    def initialize_logger(self, level, fmt):
        datefmt='%H:%M:%S'
        formatter = Formatter(fmt=fmt, datefmt=datefmt)

        handler = StreamHandler(stream=stdout)
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        self.logger.addFilter(HexLengthFilter())
        addLevelName(BotLogger.STATUS, 'STATUS')
        self.logger.setLevel(level)

    def set_verbosity(self, level):
        if level in self.verbosity_translator:
            level = self.verbosity_translator[level]
            self.logger.setLevel(level)
        # self.logger.status('Verbosity set to {}'.format(getLevelName(level)))


class HexLengthFilter(Filter):
    def filter(self, record):
        # There are 21 static characters in exec.py's log_format.
        fmt_chars = 21
        record.hex_length = '{:04x}'.format(len(record.getMessage()) + fmt_chars + len(record.levelname))
        delay()
        return True

