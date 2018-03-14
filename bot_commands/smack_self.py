from .bot_utils import print, say

def execute(**kwargs):
    # room     = kwargs['room'    ]
    # username = kwargs['username']
    message  = kwargs['message' ]
    # trigger  = kwargs['trigger' ]
    # match    = kwargs['match'   ]
    # bot_name = kwargs['bot_name']
    # direct   = kwargs['direct'  ]
    # redis    = kwargs['redis'   ]
    # logger   = kwargs['logger'  ]

    output = ''
    for i in range(message.count('derp')):
        output += ':facepalm:'
    say(output)

def usage(**kwargs):
    # room     = kwargs['room'     ]
    # username = kwargs['username' ]
    # bot_name = kwargs['bot_name' ]
    # direct   = kwargs['direct'   ]

    say('I am programmed with state-of-the-art _facepalms_ triggered by the characters `derp`.')

