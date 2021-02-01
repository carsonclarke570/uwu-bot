import os
import discord
import time

# Environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

TRIGGER_WORD = [
  'uwu', 'owo', 'ono'
]

# Cooldown
COOLDOWN = 10.0

def current_time():
    return time.time()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


cooldown_map = {}

@client.event
async def on_message(message):
    global cooldown_map

    if message.author == client.user:
        return

    if message.author in cooldown_map:
      cooldown_map[message.author]['curr'] = current_time()
    else:
        # Seed the cooldown_map
        print ('Added ' + str(message.author) + ' to cooldown map')
        cooldown_map[message.author] = {
          'curr': current_time(),
          'last': current_time() - COOLDOWN - 5.0
        }

    cool = cooldown_map[message.author]
    delta = cool['curr'] - cool['last']
    if delta >= COOLDOWN:
        cooldown_map[message.author]['last'] = cool['curr']
        for t in TRIGGER_WORD:
            if t in message.content.lower():
                await message.channel.send(t + ', comrade ' + str(message.author))
    else:
        left = COOLDOWN - delta
        print(str(message.author) + ' needs to wait ' + str(left) + ' seconds')

client.run(TOKEN)