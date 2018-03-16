from .bot_utils import say

def execute(**kwargs):
    # room     = kwargs['room'    ]
    username = kwargs['username']
    # message  = kwargs['message' ]
    # trigger  = kwargs['trigger' ]
    match    = kwargs['match'   ]
    # bot_name = kwargs['bot_name']
    # direct   = kwargs['direct'  ]
    # redis    = kwargs['redis'   ]
    # logger   = kwargs['logger'  ]

    name_line = '|                       |'
    cake = '''
         *  *  *  *  *  *
        *|_*|_*|_*|_*|_*
    .-'´|* |* |* |* |* |*`'-.
    |`-...................-´|
    |                       |
    |   _   _   _   _   _   |
  ,-|`-' '-' '-' '-' '-' '-´|-,
/´  \._                   _./  `\\
'._    `"""""""""""""""""`    _.'
   `''--.................--''´'''

    pronouns = [
        'her' ,
        'him' ,
        'it'  ,
        'them',
        'us'  ,
        'you' ,
    ]
    person = match
    if person.lower() in pronouns:
        person = 'YOU GO, YOU!'
    if person.lower() == 'me':
        person = username.upper()
    else:
        person = person.upper()
    while len(person) > len(name_line) - 4:
        person = person[:-1]
    new_name_line = '| {} |'.format(person.upper())
    while len(new_name_line) < len(name_line):
        if len(new_name_line) % 2 != 0:
            new_name_line = new_name_line.replace('| ', '|  ')
        else:
            new_name_line = new_name_line.replace(' |', '  |')

    cake = cake.replace(name_line, new_name_line)
    say('```' + cake + '```')

def usage(**kwargs):
    # room     = kwargs['room'     ]
    # username = kwargs['username' ]
    # bot_name = kwargs['bot_name' ]
    # direct   = kwargs['direct'   ]

    say('I don\'t always bake, but when I do, it\'s always a cake - `bake <person|me> a cake`.')

