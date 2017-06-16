from re import search

def execute(**kwargs):
    username = kwargs['username']
    trigger  = kwargs['trigger' ]
    message  = kwargs['message' ]

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
    person = search(trigger.exp, message).group(1)
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
    print('```' + cake + '```')

def help(**kwargs):
    bot_name = kwargs['bot_name']
    print('I don\'t always bake, but when I do, it\'s always a cake - `bake <person|me> a cake`')

