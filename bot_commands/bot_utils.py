from time import sleep

SI = '\x00\x0f'
SO = '\x00\x0e'

def delay():
    sleep(0.5)

def say(text, room=''):
    message = str(text).encode('utf-8', 'surrogateescape').decode('utf-8')
    if room:
        message = message + SI + room + SO
    print(message, end='', flush=True)
    delay()

