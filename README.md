# hubot-no-js - deploy hubot scripts using Python 3!
- Once deployed, no need to reload hubot when editing or adding scripts!

## Installation
Simply copy the contents of this repository to your bot's `scripts` folder and reload your bot.

## Configuration
Edit `exec.py` in order to change configuration values to desired specifications.

### Redis connection
`Default: inactive`

Allows connection to an existing Redis instance for data persistence across command execution.

### Logging
#### Log room
`Default: general`

Logging messages (using the built-in logger) will be sent to this room.

#### Log verbosity
`Default: 2 (errors and warnings)`

Options:
```
1 - Errors only
2 - Warnings and the above
3 - Informational messages and all of the above
4 - Debug messages and all of the above
```

### Trigger scripts
See the [Triggers](https://github.com/elespike/hubot-no-js#triggers) section below for details.

### Local path
```
Default:
/usr/lib/python3.5
/usr/lib/python3.5/lib-dynload
/usr/lib/python3.5/plat-i386-linux-gnu
/usr/lib/python3/dist-packages
/usr/lib/python35.zip
```

Allows the python process to include custom locations where to search for modules.

To get a list of local paths in a particular machine, run the following commands in the Python interpreter:
```
>>> from sys import path
>>> for p in path:
...     print(p)
...

/usr/lib/python3.5
/usr/lib/python3.5/lib-dynload
/usr/lib/python3.5/plat-i386-linux-gnu
/usr/lib/python3/dist-packages
/usr/lib/python35.zip
```

## Usage

### Commands
#### Creating commands
Simply create new python script file under `bot_commands` where the file name is the command to be executed.

For example, to create a command that responds to `marco` with `polo`:
- Create the file `bot_commands/marco.py`
- Modify the contents of the file to be:
```
def execute(**kwargs):
    print('polo')
```
That's it!

Now every time someone says `marco` in a room where the bot is active, the bot will reply with `polo`.

Please note: commands will only execute if the message starts with the command itself, whereas triggers will execute if a particular word is found anywhere in the message.
E.g., `Marco 123` **will** trigger the script; `hello there, Marco` **will not**

#### kwargs reference for commands
```
room      = kwargs['room'     ] # The room where the message was posted
username  = kwargs['username' ] # The user who posted the message
command   = kwargs['command'  ] # The command used to execute the script
arguments = kwargs['arguments'] # The list of arguments (i.e., each word in the rest of the message)
bot_name  = kwargs['bot_name' ] # The bot who is handling the message
direct    = kwargs['direct'   ] # Whether the bot was mentioned in the message (e.g., @bot)
redis     = kwargs['redis'    ] # The connected redis object
logger    = kwargs['logger'   ] # The built-in logger object
```

### Triggers
#### Creating triggers
Simply create new python script file under `bot_commands` and make the necessary changes in `exec.py`.

For example, to create a command that responds to `marco` with `polo`:
- Create the file `bot_commands/say_polo.py`
- Modify the contents of the file to be:
```
def execute(**kwargs):
    print('polo')
```
- Within `exec.py`, declare the trigger within the `trigger_scripts` variable:
```
# If a sentence does not begin with a command but is matched
# by any of the following regular expressions (with flags),
# execute the indicated script.
trigger_scripts = {
    # Example: anytime 'marco' is found in a sentence,
    # regardless of case, bot_commands/say_polo.py will be executed
    Trigger('marco', re.I): 'say_polo',
    }
```

Now every time someone says `marco` in a room where the bot is active, the bot will reply with `polo`.

Please note: triggers will execute if a particular word is found anywhere in the message, whereas commands will only execute if the message starts with the command itself.
E.g., `hello there, Marco` **will** trigger the script.

#### kwargs reference for triggers
```
room     = kwargs['room'    ] # The room where the message was posted
username = kwargs['username'] # The user who posted the message
message  = kwargs['message' ] # The entire message sent by the user
trigger  = kwargs['trigger' ] # The regex match responsible for triggering the script
bot_name = kwargs['bot_name'] # The bot who is handling the message
direct   = kwargs['direct'  ] # Whether the bot was mentioned in the message (e.g., @bot)
redis    = kwargs['redis'   ] # The connected redis object
logger   = kwargs['logger'  ] # The built-in logger object
```

### Guidance for your users
To print usage guidance when a user requests help (e.g., `@bot help`), simply add a `help()` function to your command or trigger script:
```
def help(**kwargs):
    print('marco: respond with "polo"')
```

#### kwargs reference for help functions
```
bot_name = kwargs['bot_name'] # The bot who is handling the message
username = kwargs['username'] # The user who posted the message
```

### Logging
To log messages to the log room (see the [Configuration](https://github.com/elespike/hubot-no-js#configuration) section for information on configuring the log room), use the built-in `logger` object to send Python logging events:
```
logger = kwargs['logger']
logger.debug  ('Debug message'        )
logger.info   ('Informational message')
logger.warning('Warning message'      )
logger.error  ('Error message'        )
```

In addition to Python's logging functions, there is a status() function will be issued regardless of the logging level (verbosity):
`logger.status('This will post regardless of verbosity!')`

### Debugging
If any of the scripts created under `bot_commands/` encounter errors, these errors will never be printed to chat unless explicitly sent:
```
x = 1/0 # No message sent here
try:
    x = 1/0
except ZeroDivisionError as zde:
    logger.error('Whoops! {}'.format(zde)) # Message sent here
```

### Redis
Given a pre-existing Redis instance and a proper connection, scripts under `bot_commands/` can use the built-in `redis` object to retrieve and store information from Redis:
```
redis = kwargs['redis']

# Post all available keys in the active Redis instance
print(redis.keys())

# Set 'polo' as the value for the 'marco' key
redis.set('marco', 'polo')

# Post the value of the 'marco' key
print(redis.get('marco'))
```

### Advanced messaging
To send messages to different rooms, specify the room name followed by `<+[`:
`print('{} <+[ Hello!'.format('other_room'))`

If you know the room ID of a direct message room, you can use it to have the bot send a DM. This can be a good option to act as a log room.

To issue a log message as a multi-line code block, surround the message with 2 backticks:
```
logger.debug('''
``
test: one
test: two
``
''')
```
This is due to the fact that logging messages are already formatted to have a single backtick by default.

