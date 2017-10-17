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
                room     = msg.envelope.room
                message  = trim message
                outgoing = message.split '<+['
                for value, index in outgoing
                    outgoing[index] = trim value
                if outgoing.length == 2
                    room    = outgoing[0]
                    message = outgoing[1]
                    robot.messageRoom room, message
                else if message
                    robot.messageRoom room, message

        proc.on 'exit', (code, signal) ->
            proc = null

    robot.hear /.+/, (msg) ->
        if not proc
            exec msg

    robot.router.post '/hubot/exec', (req, res) ->
        usage = '\nUsage: curl -X POST -H "Content-Type: application/json" -d \'{"room": "<room name or ID>", "cmd": "bot say hi", "as_user": "<desired user>"}\' http://127.0.0.1:8080/hubot/exec\nwhere "room" and "cmd" are required, "as_user" is optional (defaults to "EXECUTOR")\n'

        if proc
            res.send 'BUSY\n'

        try
            data    = if req.body.payload? then JSON.parse req.body.payload else req.body
            room    = data.room
            cmd     = data.cmd
            as_user = data.as_user || 'EXECUTOR'

            if not data or not room or not cmd
                res.send usage

            msg = {
                'envelope':{
                    'room': room
                    'user': {
                        'name': as_user
                    }
                    'message': cmd
                }
            }

            exec msg
            res.send 'EXECUTED!\n'

        catch err
            res.send err + usage

