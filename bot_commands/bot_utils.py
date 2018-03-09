from time import sleep

def delay():
    # To ensure correct ordering when consecutive calls are issued.
    sleep(0.02)

def say(message, room='', sep=' ', end='\n'):
    output  = '{:02x}'.format(len(room))
    # Plus one because builtins.print() ends in '\n'
    output += '{:04x}'.format(len(message) + 1)
    output += room
    output += message
    print(output, sep=sep, end=end, flush=True)
    delay()

