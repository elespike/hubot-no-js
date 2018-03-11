from .bot_utils import print, say
from importlib  import import_module
from os         import path, listdir

def execute(**kwargs):
    room      = kwargs['room'     ]
    username  = kwargs['username' ]
    command   = kwargs['command'  ]
    arguments = kwargs['arguments']
    bot_name  = kwargs['bot_name' ]
    direct    = kwargs['direct'   ]
    # redis     = kwargs['redis'    ]
    # logger    = kwargs['logger'   ]

    if not direct:
        return

    available_commands = sorted(listdir(path.dirname(path.abspath(__file__))))

    def print_usage(command=None):
        for fname in available_commands:
            proceed = True

            if command is not None and command not in fname:
                proceed = False

            skip = [
                '__init__.py',
                'template_command.py',
                'template_trigger.py'
            ]
            if proceed and fname not in skip and fname.endswith('.py'):
                module = import_module('bot_commands.{}'.format(fname[:-3]))
                if hasattr(module, 'usage'):
                    module.usage(
                        room     = room    ,
                        username = username,
                        bot_name = bot_name,
                        direct   = direct  ,
                    )

    if arguments:
        for command in arguments:
            print_usage(command=command)
    else:
        print_usage()

def usage(**kwargs):
    # room     = kwargs['room'     ]
    # username = kwargs['username' ]
    bot_name = kwargs['bot_name' ]
    direct   = kwargs['direct'   ]

    messages = [
        '[command1 command2 ...] - show usage for specified commands.',
    ]

    command = __name__.split('.')[-1]
    for message in messages:
        message = '{} {}'.format(command, message)
        if direct:
            message = '{} {}'.format(bot_name, message)

        say(message)

