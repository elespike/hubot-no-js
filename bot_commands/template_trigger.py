from .bot_utils import say

# Triggers will execute if a particular word/regex is found anywhere in the message,
# whereas commands will only execute if the message starts with the command itself.

# To add triggers, modify the appropriate configuration section in exec.py.

def execute(**kwargs):
    # room     = kwargs['room'    ]
    username = kwargs['username']
    message  = kwargs['message' ]
    trigger  = kwargs['trigger' ]
    match    = kwargs['match'   ]
    # bot_name = kwargs['bot_name']
    # direct   = kwargs['direct'  ]
    # redis    = kwargs['redis'   ]
    # logger   = kwargs['logger'  ]

def usage(**kwargs):
    # room     = kwargs['room'     ]
    # username = kwargs['username' ]
    # bot_name = kwargs['bot_name' ]
    # direct   = kwargs['direct'   ]

    say('')

