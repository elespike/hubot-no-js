from .bot_utils import *

def execute(**kwargs):
    room      = kwargs['room'     ]
    # username  = kwargs['username' ]
    # command   = kwargs['command'  ]
    arguments = kwargs['arguments']
    # bot_name  = kwargs['bot_name' ]
    direct    = kwargs['direct'   ]
    # redis     = kwargs['redis'    ]
    logger    = kwargs['logger'   ]

    if not direct:
        return

    message = ' '.join(arguments)
    if len(arguments) > 2 and arguments[-2] == ']+>':
        room = arguments[-1]
        message = ' '.join(arguments[:-2])

    say(message, room)

def usage(**kwargs):
    # room     = kwargs['room'     ]
    # username = kwargs['username' ]
    bot_name = kwargs['bot_name' ]
    direct   = kwargs['direct'   ]

    messages = [
        '<message> - repeats the message in the current room.',
        '<message> ]+> <room> - repeats the message in the specified room.',
    ]

    command = __name__.split('.')[-1]
    for message in messages:
        message = '{} {}'.format(command, message)
        if direct:
            message = '{} {}'.format(bot_name, message)

        say(message)

