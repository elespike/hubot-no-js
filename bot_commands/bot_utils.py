from time import sleep

def delay():
    # To ensure correct ordering when consecutive calls are issued.
    sleep(0.03)

def say(message, room='', end='\n'):
    message = message.encode('utf-8', 'surrogateescape')
    output  = '{:02x}'.format(len(room))
    output += '{:04x}'.format(len(message) + len(end))
    output += room
    output += message.decode('utf-8')
    print(output, end=end, flush=True)
    delay()

