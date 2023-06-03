import discord
import config
import random
import asyncio
import os
from commands import ping, chat_mode, help, coviddata, mal_search
from weather import get_weather_info
from noxactivity import set_activity
from activity import activity_dict
from smash_pass import smash_pass
from showme import show_image
from tracker import get_player_stats
from ytdownloader import yt_to_mp3

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

async def change_activity():
    while True:
        activity_id = random.choice(list(activity_dict.keys()))
        activity = activity_dict[activity_id]
        activity_name = activity['activity_name']
        activity_type = activity['activity_type']
        await client.change_presence(activity=discord.Activity(type=activity_type, name=activity_name))
        await asyncio.sleep(random.choice([10*60, 30*60, 60*60]))

@client.event
async def on_ready():
    await set_activity(client)
    print(f'Nox is ready!')
    client.loop.create_task(change_activity())

initial_server = None

@client.event
async def on_message(message):
    global initial_server

    if message.author == client.user:
        return

    if initial_server and message.guild.id != initial_server:
        return

    if client.user.mentioned_in(message):
        initial_server = message.guild.id

    command = message.content.split(' ')
    channel = message.channel
    if 'ping' in command:
        await ping(message)
    elif 'chatmode' in command:
        await chat_mode(message, client)
    elif 'helpme' in command:
        await help(message)
    elif 'covid' in command:
        await coviddata(message, *command[2:])
    elif 'mal' in command:
        await mal_search(message, *command[2:])
    elif 'weather' in command:
        location = ' '.join(command[2:])
        weather_info = get_weather_info(location)
        await channel.send(weather_info)
    elif 'sop' in command:
        await smash_pass(message)
    elif 'showme' in command:
        await show_image(message)
    elif 'track' in command:
        try:
            username = command[-1].replace('#', '%23')
            print(f"Hmm... Let me track the stats of {username} in Valorant.")
            player_stats = await get_player_stats(username)
            if player_stats is not None:
                await channel.send(player_stats)
            else:
                await channel.send("Oops! I couldn't retrieve the player stats.")
        except:
            await channel.send("Oops! Failed to retrieve the player stats.")
    elif 'ytdownload' in command:
        url = ' '.join(command[1:]).strip()
        url = url.replace('ytdownload ', '')  # Remove the "ytdownload" prefix from the URL
        print(f"Umm... I'm downloading the video from this URL: {url}")
        try:
            file_path = await yt_to_mp3(url)
            if isinstance(file_path, str) and "Failed to download" in file_path:
                await channel.send(file_path)
            else:
                wait_message = await channel.send("Please wait patiently while I convert the audio...")
                await channel.send(file=discord.File(file_path))
                # Delete the converted file from the directory
                os.remove(file_path)
                await channel.send("The file is ready for you now!")
        except Exception as e:
            await channel.send(f"Oops! Failed to download the mp3: {e}")
            
client.run(config.DISCORD_TOKEN)