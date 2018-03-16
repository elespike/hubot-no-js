from .bot_utils import say

SPLITTER = ']+>'

def execute(**kwargs):
    room      = kwargs['room'     ]
    # username  = kwargs['username' ]
    # command   = kwargs['command'  ]
    arguments = kwargs['arguments']
    # bot_name  = kwargs['bot_name' ]
    direct    = kwargs['direct'   ]
    # redis     = kwargs['redis'    ]
    # logger    = kwargs['logger'   ]

    if not direct:
        return

    message = ' '.join(arguments)
    if SPLITTER in arguments:
        split_index = arguments.index(SPLITTER)
        room    = ' '.join(arguments[split_index + 1:])
        message = ' '.join(arguments[:split_index])

    say(message, room)

def usage(**kwargs):
    # room     = kwargs['room'     ]
    # username = kwargs['username' ]
    bot_name = kwargs['bot_name' ]
    direct   = kwargs['direct'   ]

    messages = [
        '<message> - repeats the message in the current room.',
        '<message> {} <room> - repeats the message in the specified room.'.format(SPLITTER),
    ]

    command = __name__.split('.')[-1]
    for message in messages:
        message = '{} {}'.format(command, message)
        if direct:
            message = '{} {}'.format(bot_name, message)

        say(message)

