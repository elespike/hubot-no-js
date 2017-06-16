from re import search

def execute(**kwargs):
    command   = kwargs['command'  ]
    arguments = kwargs['arguments']
    logger    = kwargs['logger'   ]

    if not arguments:
        return

    def fail(msg=''):
        print('Does not compute!', flush=True)
        logger.error('Command "{}" failed with expression "{}"! {}'.format(command, operation, msg))

    operation = ''.join(arguments)

    match = search(r'((\()*[a-fA-F0-9x~.]+(\))*[-+*/%^&|<>]?[*<>]?([!=]=)?)+', operation)
    if match:
        results = []
        try:
            result = eval(operation)
            results.append(result)

            if type(result) == int:
                if result < 0:
                    # Two's complement
                    result = abs(result) - (1 << (len(str(bin(result))) - 2)) # -2 to account for '0b'
                results.append(hex(result).replace('-', ''))
                results.append(bin(result).replace('-', ''))

            for r in results:
                print('`{}`'.format(r), end=' ')
        except Exception as e:
            fail(e)
    else:
        fail()

def help(**kwargs):
    bot_name = kwargs['bot_name']
    print('calc <math, bool or bin operation> - calculate the given operation. Parentheses as well as "0x" and "0b" notations are supported.')

