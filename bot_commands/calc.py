from .bot_utils import *
from re         import search

def execute(**kwargs):
    # room      = kwargs['room'     ]
    # username  = kwargs['username' ]
    command   = kwargs['command'  ]
    arguments = kwargs['arguments']
    # bot_name  = kwargs['bot_name' ]
    # direct    = kwargs['direct'   ]
    # redis     = kwargs['redis'    ]
    logger    = kwargs['logger'   ]

    if not arguments:
        return

    def fail(msg=''):
        say('Does not compute!', flush=True)
        logger.error('Command "{}" failed with expression "{}"! {}'.format(command, operation, msg))

    operation = ''.join(arguments)

    match = search(r'((\()*[a-fA-F0-9x~.]+(\))*[-+*/%^&|<>]?[*<>]?([!=]=)?)+', operation)
    if match:
        results = []
        try:
            result = eval(operation)
            results.append(result)

            if type(result) == int:
                if result < 0:
                    # Two's complement
                    result = abs(result) - (1 << (len(str(bin(result))) - 2)) # -2 to account for '0b'
                results.append(hex(result).replace('-', ''))
                results.append(bin(result).replace('-', ''))

            for r in results:
                say('`{}`'.format(r), end=' ')
        except Exception as e:
            fail(e)
    else:
        fail()

def usage(**kwargs):
    # room     = kwargs['room'     ]
    # username = kwargs['username' ]
    bot_name = kwargs['bot_name' ]
    direct   = kwargs['direct'   ]

    messages = [
        '<operation> - calculate the given arithmetic, boolean or binary operation. Parentheses as well as "0x" and "0b" notations are supported.',
    ]

    command = __name__.split('.')[-1]
    for message in messages:
        message = '{} {}'.format(command, message)
        if direct:
            message = '{} {}'.format(bot_name, message)

        say(message)

