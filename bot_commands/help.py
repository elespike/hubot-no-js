from importlib import import_module
from os import path, listdir

def execute(**kwargs):
    if not kwargs['direct']:
        return

    bot_name = kwargs['bot_name']
    room     = kwargs['room'    ]
    username = kwargs['username']

    available_commands = sorted(listdir(path.dirname(path.abspath(__file__))))

    def print_help(command=None):
        for fname in available_commands:
            proceed = True

            if command is not None and command not in fname:
                proceed = False

            if proceed and fname.endswith('.py') and fname != '__init__.py':
                module = import_module('bot_commands.{}'.format(fname[:-3]))
                if hasattr(module, 'help'):
                    module.help(
                        bot_name = bot_name,
                        room     = room    ,
                        username = username,
                    )

    arguments = kwargs['arguments']
    if arguments:
        for command in arguments:
            print_help(command=command)
    else:
        print_help()

def help(**kwargs):
    bot_name = kwargs['bot_name']
    print(bot_name, 'help [command1 command2 ...] - show usage for specified command(s)')

