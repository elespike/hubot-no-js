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

        SI = 15
        SO = 14
        proc.stdout.on 'data', (data) ->
            while (sii = data.indexOf(SI)) > 0 \
            and   (soi = data.indexOf(SO)) > 0 \
            and data[sii - 1] is 0             \
            and data[soi - 1] is 0
                message = data.slice(0      , sii - 1).toString('utf-8')
                room    = data.slice(sii + 1, soi - 1).toString('utf-8')
                robot.messageRoom room, message
                data = data.slice(soi + 1)

            message = data.toString('utf-8')
            if message
                robot.messageRoom msg.envelope.room, message
                

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

