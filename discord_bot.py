import subprocess
import discord
from subprocess import Popen, PIPE
import os
import threading
from flask import Flask
p = None
app = Flask(__name__)
client = discord.Client()
@client.event
async def on_ready():
    print('Online')

@app.route('/terminate')
def terminate():
    global p
    p.terminate()
    return 'OK'

subprocess.Popen(['python3', 'discord_bot/discord_bot2.py'])
threading.Thread(target=app.run, kwargs=dict(host='0.0.0.0', port=7665)).start()

def embed(type, data=None):
    if type == 'run':
        return discord.Embed(
            title='Running {}...'.format(data[0]),
            color=discord.Color.from_rgb(255, 0, 0),
            description='Output:\n' + data[1]
        )
    elif type == 'finished':
        return discord.Embed(
            title='Program finished',
            color=discord.Color.from_rgb(0, 255, 0),
            description=data
        )
    if type == 'filenotfound':
        return discord.Embed(
            title='File not found',
            color=discord.Color.from_rgb(255, 0, 0),
            description=data + 'doesnt exist'
        )
    else:
        raise KeyError


@client.event
async def on_message(message):
    global p
    channel = message.channel
    args = message.content.split(' ')
    content = str(message.content)
    content_split_by_line = content.split('\n')
    code = ''
    x = 0
    for line in content_split_by_line:
        if line.startswith('```'):
            pass
        elif line.startswith('^run_code_'):
            pass
        else:
            code = code + '\n' + line
        x = x + 1
    if args[0] == '^run_py':
        msg = await channel.send(embed=embed('run', [args[1], '']))
        p_args = args
        p_args[0] = 'python3'
        if os.path.exists(p_args[1]):
            p = Popen(p_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output = ''
            for line in iter(p.stdout.readline, b''):
                output = output + line.decode('utf-8')
                await msg.edit(embed=embed('run', [args[1], output]))
            
            await msg.edit(embed=embed('finished', 'Output:\n{}'.format(output)))
        else:
            await msg.edit(embed=embed('filenotfound', args[1]))
    if content.startswith('^run_code_py'):
        f = open('temp.py', 'w+')
        f.write(code)
        f.close()
        p_args = []
        msg = await channel.send(embed=embed('run', ['code', '']))
        p_args.append('python3')
        p_args.append('temp.py')
        print(p_args)
        p = Popen(p_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output = ''
        for line in iter(p.stdout.readline, b''):
            output = output + line.decode('utf-8')
            await msg.edit(embed=embed('run', ['code', output]))
        os.system('rm temp.py')
        await msg.edit(embed=embed('finished', 'Output:\n{}'.format(output)))
    if content.startswith('^run_code_c'):
        f = open('temp.c', 'w+')
        f.write(code)
        f.close()
        os.system('gcc temp.c -o temp')
        p_args = []
        msg = await channel.send(embed=embed('run', ['code', '']))
        p_args.append('./temp')
        print(p_args)
        p = Popen(p_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output = ''
        for line in iter(p.stdout.readline, b''):
            output = output + line.decode('utf-8')
            await msg.edit(embed=embed('run', ['code', output]))
        os.system('rm temp')
        os.system('rm temp.c')
        await msg.edit(embed=embed('finished', 'Output:\n{}'.format(output)))
    if args[0] == '^run_exec':
        msg = await channel.send(embed=embed('run', [args[1], '']))
        p_args = args
        p_args[1] = './{}'.format(p_args[1])
        p_args1 = p_args[1].replace('./', '')
        del p_args[0]
        if os.path.exists(p_args1):
            p = Popen(p_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output = ''
            for line in iter(p.stdout.readline, b''):
                output = output + line.decode('utf-8')
                await msg.edit(embed=embed('run', [p_args1, output]))
            
            await msg.edit(embed=embed('finished', 'Output:\n{}'.format(output)))
        else:
            await msg.edit(embed=embed('filenotfound', p_args1))
    if args[0] == '^terminate':
        p.terminate()


client.run('token')