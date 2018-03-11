from .bot_utils   import print, say
from base64       import b64decode
from binascii     import hexlify
from urllib.parse import unquote

def b64d(data):
    data = b64decode(data.encode())
    try:
        data = data.decode()
    except UnicodeDecodeError:
        data = hexlify(data)
        data = data.decode()
        data = '0x' + data
    return data


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
        'base64': b64d   ,
        'b64'   : b64d   ,
        'url'   : unquote,
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
        '<data> <algorithm> - decode data using the specified algorithm (base64 or b64, url).',
    ]

    command = __name__.split('.')[-1]
    for message in messages:
        message = '{} {}'.format(command, message)
        if direct:
            message = '{} {}'.format(bot_name, message)

        say(message)

