def execute(**kwargs):
    if not kwargs['direct']:
        return
    print(' '.join(kwargs['arguments']))

def help(**kwargs):
    bot_name = kwargs['bot_name']
    print(bot_name, ' say <message> - repeats the message in the current room')
    print(bot_name, ' say <room> ˂+[ <message> - repeats the message in the specified room')

