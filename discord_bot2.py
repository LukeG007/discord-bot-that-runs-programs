import subprocess
import discord
import subprocess
import requests
p = None
client = discord.Client()
@client.event
async def on_ready():
    print('Online')


@client.event
async def on_message(message):
    args = message.content.split(' ')
    if message.content == '^terminate':
        requests.get('http://localhost:7665/terminate')
    if args[0] == '^clone_repo':
        repo = args[1]
        embed = discord.Embed(
            title='Cloning repository...',
            color=discord.Color.from_rgb(255, 0, 0),
        )
        embed2 = discord.Embed(
            title='Cloned repository',
            color=discord.Color.from_rgb(0, 255, 0)
        )
        msg = await message.channel.send(embed=embed)
        p = subprocess.Popen(['git', 'clone', repo])
        while p.poll() is None:
            pass
        await msg.edit(embed=embed2)




client.run('ODczMzg5NzYyMjAxOTM5OTk4.YQ3tmg.jujx22hbFCPEluL9DnCVXZfQZyE')