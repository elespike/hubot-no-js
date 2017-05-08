from logging import (
    Formatter    ,
    StreamHandler,
    addLevelName ,
    getLevelName ,
    getLogger    ,
)
from random import randint
from sys import stdout

class Logspike:
    STATUS = 9001
    while 'Level' not in getLevelName(STATUS):
        STATUS = randint(100, 10000)
    def __init__(self, level=20, fmt=None):
        self.logger = getLogger(__name__)

        self.verbosity_translator = {
            1: 40, # ERROR
            2: 30, # WARNING
            3: 20, # INFO
            4: 10, # DEBUG
        }

        self.initialize_logger(level, fmt)

        def status(message, *args, **kwargs):
            self.logger.log(Logspike.STATUS, message, *args, **kwargs)
        self.logger.status = status

    def initialize_logger(self, level, fmt):
        if fmt is None:
            fmt='%(asctime)s:%(msecs)03d [%(levelname)s] %(message)s\n'
        datefmt='%H:%M:%S'
        formatter = Formatter(fmt=fmt, datefmt=datefmt)

        handler = StreamHandler(stream=stdout)
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)
        addLevelName(Logspike.STATUS, 'STATUS')
        self.logger.setLevel(level)

    def set_verbosity(self, level):
        if level in self.verbosity_translator:
            level = self.verbosity_translator[level]
            self.logger.setLevel(level)
        # self.logger.status('Verbosity set to {}'.format(getLevelName(level)))

