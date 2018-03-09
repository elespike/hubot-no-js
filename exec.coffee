{spawn} = require 'child_process'

module.exports = (robot) ->

    # Utility function to trim leading and trailing whitespace.
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

        proc.stdout.pause()

        proc.stdout.on 'readable', () ->
            while len_bytes = proc.stdout.read(6)
                hex_len  = len_bytes.toString()
                room_len = parseInt(hex_len.slice(0, 2), 16)
                msg_len  = parseInt(hex_len.slice(2   ), 16)

                if room_len > 0
                    room = proc.stdout.read(room_len)
                    room = room.toString()
                else
                    room = msg.envelope.room

                if msg_len < 1
                    continue
                message = proc.stdout.read(msg_len)
                message = message.toString()

                robot.messageRoom room, message


    robot.hear /.+/, (msg) ->
        exec msg


    robot.router.post '/hubot/exec', (req, res) ->
        usage = '\nUsage: curl -X POST -H "Content-Type: application/json" -d \'{"room": "<room name or ID>", "cmd": "bot say hi", "as_user": "<desired user>"}\' http://127.0.0.1:8080/hubot/exec\nwhere "room" and "cmd" are required, "as_user" is optional (defaults to "EXECUTOR")\n'

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

