# Commands will only execute if the message starts with the command itself,
# whereas triggers will execute if a particular word is found anywhere in the message.

# To add commands, simply create a python script in this directory.

def execute(**kwargs):
    room      = kwargs['room'     ]
    username  = kwargs['username' ]
    command   = kwargs['command'  ]
    arguments = kwargs['arguments']
    bot_name  = kwargs['bot_name' ]
    direct    = kwargs['direct'   ]
    redis     = kwargs['redis'    ]
    logger    = kwargs['logger'   ]

def help(**kwargs):
    bot_name = kwargs['bot_name']
    username = kwargs['username']
    return

