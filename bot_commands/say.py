def execute(**kwargs):
    if not kwargs['direct']:
        return
    logger = kwargs['logger']

    message = ' '.join(kwargs['arguments'])

    try:
        # This allows for user messages to contain unicode characters
        message = message.encode('utf-8', 'surrogateescape')
        message = message.decode('utf-8')

        print(message)
    except ValueError as ve:
        logger.error('ValueError: {}'.format(ve))

def help(**kwargs):
    bot_name = kwargs['bot_name']
    print(bot_name, 'say <message> - repeats the message in the current room')
    print(bot_name, 'say <room> ˂+[ <message> - repeats the message in the specified room')

