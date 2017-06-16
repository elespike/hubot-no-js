from base64 import b64encode
from binascii import unhexlify, Error as binascii_error
from urllib.parse import quote

def b64e(data):
    if data.startswith('0x'):
        try:
            data = data[2:]
            data = unhexlify(data)
        except binascii_error:
            data = data.encode()
    else:
        data = data.encode()
    return b64encode(data).decode()

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
        BASE64: b64e,
        URL   : quote,
    }

    if algo not in algorithms:
        print('Unknown algorithm: {}'.format(algo))
        return

    print(algorithms[algo](data))

def help(**kwargs):
    bot_name = kwargs['bot_name']
    print(bot_name, 'encode <data> <base64|url> - encode <data> using specified algorithm')

