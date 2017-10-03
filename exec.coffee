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
                else if message
                    room = msg.envelope.room
                robot.messageRoom room, message

        proc.on 'exit', (code, signal) ->
            proc = null

    robot.hear /.+/, (msg) ->
        if not proc
            exec msg

    robot.router.post '/hubot/exec/:room', (req, res) ->
        if proc
            res.send 'BUSY\n'
            return

        try
            room = req.params.room
            data = if req.body.payload? then JSON.parse req.body.payload else req.body
            cmd  = data.cmd

            msg = {
                'envelope':{
                    'room': room
                    'user': {
                        'name': 'EXECUTOR'
                    }
                    'message': cmd
                }
            }

            exec msg

            res.send 'OK\n'

        catch err
            res.send err

