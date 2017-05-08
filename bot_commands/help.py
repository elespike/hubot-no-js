from importlib import import_module
from os import path, listdir

def execute(**kwargs):
    if not kwargs['direct']:
        return

    bot_name = kwargs['bot_name']
    username = kwargs['username']

    for fname in sorted(listdir(path.dirname(path.abspath(__file__)))):
        if fname.endswith('.py') and fname != '__init__.py':
            module = import_module('bot_commands.{}'.format(fname[:-3]))
            if hasattr(module, 'help'):
                module.help(
                    bot_name=bot_name,
                    username=username,
                )

