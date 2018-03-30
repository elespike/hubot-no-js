from time import sleep

STX = '\x00\x02'
ETX = '\x00\x03'
SO  = '\x00\x0e'
SI  = '\x00\x0f'

def delay():
    sleep(0.5)

def issue(message):
    print(message, end='', flush=True)
    delay()

def parse_json(**kwargs):
    room      = kwargs['room'     ]
    username  = kwargs['username' ]
    command   = kwargs['command'  ]
    arguments = kwargs['arguments']
    bot_name  = kwargs['bot_name' ]
    redis     = kwargs['redis'    ]
    logger    = kwargs['logger'   ]

##################################### Configuration ######################################

    for key, value in arguments.items():
        # Add logic here to extract messages and other values
        # from the arguments dictionary, which is built from JSON received
        # via HTTP requests to Hubot's built-in listener.

        # Example
        if key == 'desired_key':
            message = value
            # Assuming the message is formatted as a command; e.g., 'mybot say hi',
            # one may use parse_message() to obtain each piece in its own variable:
            command, arguments, direct = parse_message(message, bot_name)

##########################################################################################

    values = {}
    values['room'     ] = room
    values['username' ] = username
    values['command'  ] = command
    values['arguments'] = arguments
    values['bot_name' ] = bot_name
    values['direct'   ] = direct
    return values

def parse_message(message, bot_name):
    bot_name = bot_name.lower()
    arguments = message.split(' ')
    if bot_name in arguments[0].lower():
        arguments.pop(0)
    command = arguments.pop(0).strip()
    direct  = message.lower().replace('@', '', 1).startswith(bot_name)
    return command, arguments, direct

def say(text, room=''):
    message = str(text).encode('utf-8', 'surrogateescape').decode('utf-8')
    if room:
        message = message + SI + room + SO
    issue(message)

def send(text):
    message = str(text).encode('utf-8', 'surrogateescape').decode('utf-8')
    message = STX + message + ETX
    issue(message)

