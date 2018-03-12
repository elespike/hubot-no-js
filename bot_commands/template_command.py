from .bot_utils import print, say

# Commands will only execute if the message starts with the command itself,
# whereas triggers will execute if a particular word/regex is found anywhere in the message.

# To add commands, simply create a python script in this directory.

def execute(**kwargs):
    # room      = kwargs['room'     ]
    # username  = kwargs['username' ]
    command   = kwargs['command'  ]
    arguments = kwargs['arguments']
    bot_name  = kwargs['bot_name' ]
    direct    = kwargs['direct'   ]
    # redis     = kwargs['redis'    ]
    # logger    = kwargs['logger'   ]

    if not direct:
        return

def usage(**kwargs):
    # room     = kwargs['room'     ]
    # username = kwargs['username' ]
    bot_name = kwargs['bot_name' ]
    direct   = kwargs['direct'   ]

    messages = [
        '',
    ]

    command = __name__.split('.')[-1]
    for message in messages:
        message = '{} {}'.format(command, message)
        if direct:
            message = '{} {}'.format(bot_name, message)

        say(message)

