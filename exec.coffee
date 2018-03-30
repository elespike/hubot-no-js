{spawn} = require 'child_process'

module.exports = (robot) ->

    # Utility function to trim leading and trailing whitespace.
    trim = (str) ->
        return str.replace /^\s+|\s+$/g, ''


    exec = (msg, res=null) ->
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

        STX = 2
        ETX = 3
        SO = 14
        SI = 15

        proc.stdout.on 'data', (data) ->
            while (zi = data.indexOf(0)) >= 0
                if data[zi + 1] is SI
                    si = data.indexOf(SI)
                    so = data.indexOf(SO)
                    if si < 0 or so < 0 or data[so - 1] isnt 0
                        break
                    message = data.slice(0     , zi    ).toString('utf-8')
                    room    = data.slice(si + 1, so - 1).toString('utf-8')
                    robot.messageRoom room, message
                    data = data.slice(so + 1)

                if res and data[zi + 1] is STX
                    stx = data.indexOf(STX)
                    etx = data.indexOf(ETX)
                    if stx < 0 or etx < 0 or data[etx - 1] isnt 0
                        break
                    message = data.slice(stx + 1, etx - 1).toString('utf-8')
                    if not res.finished
                        res.setHeader('Content-Type', 'application/json');
                        res.send message
                    data = data.slice(etx + 1)

            message = data.toString('utf-8')
            if message
                robot.messageRoom msg.envelope.room, message

        proc.stdout.on 'end', () ->
            if res and not res.finished
                res.send 'EXECUTED!\n'
                

    robot.hear /.+/, (msg) ->
        exec msg


    robot.router.post '/hubot/exec', (req, res) ->
        usage = '\nUsage: curl -X POST -H "Content-Type: application/json" -d \'{"room": "<room name or ID>", "cmd": "bot say hi", "as_user": "<desired user>"}\' http://127.0.0.1:8080/hubot/exec\nwhere "room" and "cmd" are required, "as_user" is optional (defaults to "EXECUTOR")\n'

        try
            data = if req.body.payload? then JSON.parse req.body.payload else req.body

            if not data
                res.send usage
                return

            room    = data.room    || ''
            cmd     = data.cmd     || JSON.stringify(data)
            as_user = data.as_user || 'EXECUTOR'

            msg = {
                'envelope':{
                    'room': room
                    'user': {
                        'name': as_user
                    }
                    'message': cmd
                }
            }

            exec msg, res

        catch err
            res.send err + usage

