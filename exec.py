#! /usr/bin/python3

from bot_commands.bot_utils import SI, SO, parse_json, parse_message
from botlogger   import BotLogger
from collections import namedtuple
from importlib   import import_module
from json        import loads, JSONDecodeError
from sys         import argv, path, stdout
import re

Trigger = namedtuple('Trigger', 'exp, flags')

##################################### Configuration ######################################

# Redis connection (see https://redis-py.readthedocs.io/en/latest/).
# To activate, comment the next line and uncomment the following 2.
redis = {}
# from redis import Redis
# redis = Redis()

# Room where to send logging messages.
log_room = 'general'
# Verbosity: 1-Error 2-Warning 3-Info 4-Debug
verbosity = 2

# If a sentence does not begin with a command but is matched
# by any of the following regular expressions (with flags),
# execute the indicated script.
trigger_scripts = {
    # Example: if a sentence contains at least once instance of 'derp',
    # regardless of case, bot_commands/smack_self.py will be executed.
    Trigger('.*derp.*', re.I): 'smack_self',
    # Example: for each instance of 'bake [word] a cake' in a sentence,
    # regardless of case, bot_commands/the_cake_is_a_lie.py will be executed.
    Trigger('bake (\w+) a cake', re.I): 'the_cake_is_a_lie',
}

# Local machine paths where to search for additional modules.
local_path = [
    '/usr/lib/python3.5'                      ,
    '/usr/lib/python3.5/lib-dynload'          ,
    '/usr/lib/python3.5/plat-i386-linux-gnu'  ,
    '/usr/lib/python3.5/plat-x86_64-linux-gnu',
    '/usr/lib/python3/dist-packages'          ,
    '/usr/lib/python35.zip'                   ,
]

##########################################################################################

log_format = '`%(asctime)s:%(msecs)03d [%(levelname)s]` `%(message)s`{}{}{}'
log_format = log_format.format(SI, log_room, SO)
log_manager = BotLogger(log_format)
log_manager.set_verbosity(verbosity)
logger = log_manager.logger

path.extend(local_path)

room     = argv[1] or log_room
username = argv[2]
message  = argv[3].strip()
bot_name = argv[4]

try:
    arguments = loads(message)
    command   = 'parse_json'

    values = parse_json(
        room      = room     ,
        username  = username ,
        command   = command  ,
        arguments = arguments,
        bot_name  = bot_name ,
        redis     = redis    ,
        logger    = logger   ,
    )

    room      = values['room'     ]
    username  = values['username' ]
    command   = values['command'  ]
    arguments = values['arguments']
    bot_name  = values['bot_name' ]
    direct    = values['direct'   ]

except JSONDecodeError:
    command, arguments, direct = parse_message(message, bot_name)

debug_args = '''``
  room:\t{}
  user:\t{}
   msg:\t{}
   cmd:\t{}
  args:\t{}
   bot:\t{}
direct:\t{}
``'''
debug_args = debug_args.format(
        room     ,
        username ,
        message  ,
        command  ,
        arguments,
        bot_name ,
        direct   ,
)
logger.debug(debug_args)

try:
    module = import_module('bot_commands.{}'.format(command))
    module.execute(
        room      = room     ,
        username  = username ,
        command   = command  ,
        arguments = arguments,
        bot_name  = bot_name ,
        direct    = direct   ,
        redis     = redis    ,
        logger    = logger   ,
    )

except Exception as cmd_fail:
    logger.debug('Failed to execute command: {}'.format(cmd_fail))
    for trigger, _command in trigger_scripts.items():
        matches = re.findall(trigger.exp, message, trigger.flags)

        if not matches:
            continue

        try:
            module = import_module('bot_commands.{}'.format(_command))
        except Exception as trigger_fail:
            logger.debug('Failed to execute trigger: {}'.format(trigger_fail))
            continue

        for match in matches:
            module.execute(
                room     = room    ,
                username = username,
                message  = message ,
                trigger  = trigger ,
                match    = match   ,
                bot_name = bot_name,
                direct   = direct  ,
                redis    = redis   ,
                logger   = logger  ,
            )

