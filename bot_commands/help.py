from importlib import import_module
from os import path, listdir

def execute(**kwargs):
    if not kwargs['direct']:
        return

    bot_name = kwargs['bot_name']
    room     = kwargs['room'    ]
    username = kwargs['username']

    def print_help(command):
        module = import_module('bot_commands.{}'.format(command))
        if hasattr(module, 'help'):
            module.help(
                bot_name = bot_name,
                room     = room    ,
                username = username,
            )

    def print_all_help():
        for fname in sorted(listdir(path.dirname(path.abspath(__file__)))):
            if fname.endswith('.py') and fname != '__init__.py':
                print_help(fname[:-3])

    arguments = kwargs['arguments']
    if arguments:
        for command in arguments:
            print_help(command)
    else:
        pass
        print_all_help()

def help(**kwargs):
    bot_name = kwargs['bot_name']
    print(bot_name, 'help [command1 command2 ...] - show usage for specified command(s)')

