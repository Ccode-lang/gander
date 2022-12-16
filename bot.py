import guilded
from better_profanity import profanity
import config
import os
import datetime

client = guilded.Client()

@client.event
async def on_ready():
    log(f'We have logged in as {client.user}')

def log(line):
    t = datetime.datetime.now()
    t = t.strftime("%d/%m/%Y %H:%M:%S")
    line = "[" + t + "] " + line
    print(line)
    file = open(os.path.join("log", "log.txt"), "a")
    file.write(line + os.linesep)
    file.close()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    check = "".join(ch for ch in message.content if ch.isalnum())

    if profanity.contains_profanity(check) or profanity.contains_profanity(message.content):
        channel = guilded.utils.get(message.guild.text_channels, name = config.modlog)
        log(message.author.name + ' said: "' + message.content + '" on server "' + message.guild.name + '"')
        if not channel == None:
            await channel.send(message.author.name + ' said: "' + message.content + '" on server "' + message.guild.name + '"')
        try:
            await message.delete()
        except:
            log("Invalid perms")
    elif message.content.startswith('!echo '):
        send = message.content[6:]
        log(message.author.name + ' echoed: "' + message.content[6:] + '" on server "' + message.guild.name + '"')
        await message.channel.send(send)
    elif message.content.lower() == "gm":
        await message.channel.send("The " + message.author.name + " has awoken!")
    elif message.content.lower() == "gn":
        await message.channel.send("The " + message.author.name + " has gone into a deep slumber.")


client.run(config.token)