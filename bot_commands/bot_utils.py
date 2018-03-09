from time import sleep

def delay():
    # To ensure correct ordering when consecutive calls are issued.
    sleep(0.02)

def say(message, room='', end='\n'):
    output  = '{:02x}'.format(len(room))
    output += '{:04x}'.format(len(message) + len(end))
    output += room
    output += message
    print(output, end=end, flush=True)
    delay()

