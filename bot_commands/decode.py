from base64 import b64decode
from binascii import hexlify
from urllib.parse import unquote

def b64d(data):
    data = b64decode(data.encode())
    try:
        data = data.decode()
    except UnicodeDecodeError:
        data = hexlify(data)
        data = data.decode()
        data = '0x' + data
    return data

def execute(**kwargs):
    if not kwargs['direct']:
        return
    try:
        args = kwargs['arguments']
        data = ' '.join(args[:-1])
        algo = args[-1].lower()
    except IndexError:
        print('Missing options!')
        return

    BASE64 = 'base64'
    URL    = 'url'
    algorithms = {
        BASE64: b64d,
        URL   : unquote,
    }

    if algo not in algorithms:
        print('Unknown algorithm: {}'.format(algo))
        return

    print(algorithms[algo](data))

def help(**kwargs):
    bot_name = kwargs['bot_name']
    print(bot_name, 'decode example [base64|url]')

