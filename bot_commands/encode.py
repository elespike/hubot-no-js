from .bot_utils   import say
from base64       import b64encode
from binascii     import unhexlify, Error as binascii_error
from urllib.parse import quote

def b64e(data):
    if data.startswith('0x'):
        try:
            data = data[2:]
            data = unhexlify(data)
        except binascii_error:
            data = data.encode()
    else:
        data = data.encode()
    return b64encode(data).decode()

def execute(**kwargs):
    # room      = kwargs['room'     ]
    # username  = kwargs['username' ]
    command   = kwargs['command'  ]
    arguments = kwargs['arguments']
    # bot_name  = kwargs['bot_name' ]
    direct    = kwargs['direct'   ]
    # redis     = kwargs['redis'    ]
    # logger    = kwargs['logger'   ]

    if not direct or not arguments:
        return

    data = ' '.join(arguments[:-1])
    algo = arguments[-1].lower()

    algorithms = {
        'base64': b64e ,
        'b64'   : b64e ,
        'url'   : quote,
    }

    if algo not in algorithms:
        say('Unknown algorithm: {}'.format(algo))
        return

    say(algorithms[algo](data))


def usage(**kwargs):
    # room     = kwargs['room'     ]
    # username = kwargs['username' ]
    bot_name = kwargs['bot_name' ]
    direct   = kwargs['direct'   ]

    messages = [
        '<data> <algorithm> - encode data using the specified algorithm (base64 or b64, url).',
    ]

    command = __name__.split('.')[-1]
    for message in messages:
        message = '{} {}'.format(command, message)
        if direct:
            message = '{} {}'.format(bot_name, message)

        say(message)

