{spawn} = require 'child_process'

module.exports = (robot) ->
    proc = null

    # Trim leading and trailing whitespace
    trim = (str) ->
        return str.replace /^\s+|\s+$/g, ''

    exec = (msg) ->
        # Prefer the alias
        bot_name = robot.alias
        if not bot_name
            bot_name = robot.name

        proc_args = [
            __dirname + '/exec.py'
            msg.envelope.room
            msg.envelope.user.name
            msg.envelope.message
            bot_name
        ]
        process.env.PYTHONIOENCODING = 'utf-8'
        proc = spawn 'python3', proc_args

        proc.stdout.on 'data', (data) ->
            room = msg.envelope.room
            data = data.toString()

            # In case of quickly-repeated logging messages
            messages = data.split ']+>'
            for message in messages
                message = trim message
                outgoing = message.split '<+['
                for value, index in outgoing
                    outgoing[index] = trim value
                if outgoing.length == 2
                    room = outgoing[0]
                    message = outgoing[1]
                    robot.messageRoom room, message
                else if message
                    msg.send message

        proc.on 'exit', (code, signal) ->
            proc = null

    robot.hear /.+/, (msg) ->
        if not proc
            exec msg

