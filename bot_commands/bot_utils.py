from builtins import print as the_print
from sys      import stdout
from time     import sleep


class _Message:
    def __init__(self, text='', room=''):
        self.text = text
        self.room = room

    @staticmethod
    def delay():
        # To ensure correct ordering when consecutive calls are issued.
        sleep(0.03)

    def __str__(self):
        room = self.room.encode('utf-8', 'surrogateescape')
        text = self.text.encode('utf-8', 'surrogateescape')

        formatted_text = '{}{}{}{}'.format(
            '{:02x}'.format(len(room)),
            '{:04x}'.format(len(text)),
            room.decode('utf-8'),
            text.decode('utf-8')
        )
        self.delay()
        return formatted_text


def print(*objects, sep=' ', end='\n', file=stdout, flush=False):
    message = _Message(sep.join(objects) + end)
    the_print(message, sep='', end='', file=file, flush=flush)

def say(text, room=''):
    message = _Message(text, room)
    the_print(message, end='', flush=True)

