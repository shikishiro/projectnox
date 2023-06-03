import asyncio
import discord
import time
import requests
from bs4 import BeautifulSoup
from personality import get_personality_prompt
from gpt import chatgpt

async def ping(message):
    start_time = time.time()
    await message.channel.send(":ping_pong: Pong! How can I assist you?")
    latency = (time.time() - start_time) * 1000
    await message.channel.send(f"Latency: {latency:.2f}ms")

async def chat_mode(message, client):
    reply_message = "Alright, let's chat! Just type 'chatstop' when you want to stop."
    await message.channel.send(reply_message)

    with open('logs.txt', 'a') as f:
        f.write(f'--- Chat started on {message.guild} ---\n')

    while True:
        try:
            user_message = await client.wait_for('message', timeout=60.0, check=lambda m: m.author == message.author and not m.author.bot)
        except asyncio.TimeoutError:
            reply_message = 'Alright, let\'s take a break from chatting.'
            await message.channel.send(reply_message)

            with open('logs.txt', 'a') as f:
                f.write(f'--- Chat stopped on {message.guild} ---\n')
            break

        if 'chatstop' in user_message.content.lower():
            reply_message = 'Okay, let\'s stop chatting for now.'
            await message.channel.send(reply_message)

            with open('logs.txt', 'a') as f:
                f.write(f'--- Chat stopped on {message.guild} ---\n')
            break

        personality = get_personality_prompt()

        bot_response = await chatgpt(personality, user_message.content)

        await message.channel.send(f"{bot_response}")

        with open('logs.txt', 'a') as f:
            f.write(f'user said: {user_message.content}\nnox said: {bot_response}')

async def help(message):
    command_list = [
        "⚡ **ping**: Umm... you can check out my latency, if you want.",
        "💬 **chatmode**: H-Hey! We can, umm, chat if you'd like... about programming or anything tech-related.",
        "📚 **mal <media type, title>**: I can... umm... help you find information about an anime or manga you're interested in.",
        "🌍 **covid <country>**: Oh, COVID-19... I... don't like it either. I can give you the latest statistics for a country, if you want.",
        "🌤️ **weather <location>**: I-I can give you the weather for a location. Just let me know where...",
        "🔥 **sop <attach an image>**: Oh! I-I can tell you if I'd, umm, smash or pass... Just send me a picture.",
        "🖼️ **showme <keyword>**: I enjoy looking at images... L-Let me find some for you based on a keyword.",
        "🎮 **track <Valorant username>**: I'm... curious to see how good you are at Valorant. I can track your stats... if you'd like.",
        "🔊 **ytdownload <YouTube URL>**: I can... help you download a YouTube video and convert it to MP3. If you want...",
        "❓ **helpme**: I-I'm here to help! Just let me know if you need anything...",
    ]

    embed = discord.Embed(
        title="Nox Command List",
        description="Here are the commands you can use with me:",
        color=discord.Color.blue()
    )

    # Set the bot's avatar as the thumbnail
    embed.set_thumbnail(url=message.guild.me.avatar.url)

    for command in command_list:
        embed.add_field(name=command.split(' ', 1)[0], value=command.split(' ', 1)[1], inline=False)

    await message.channel.send(embed=embed)

    
async def coviddata(context, *args):
    if len(args) == 0:
        await context.channel.send(f"Um, you didn't specify a country. You said: {' '.join(context.content.split()[1:])}")
    else:
        country = " ".join(args).title()
        url = f"https://api.covid19api.com/live/country/{country}/status/confirmed"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                latest_data = data[-1]
                confirmed = latest_data["Confirmed"]
                deaths = latest_data["Deaths"]
                recovered = latest_data["Recovered"]
                active = latest_data["Active"]
                message = f"Latest COVID-19 statistics for {country}:\nConfirmed Cases: {confirmed}\nDeaths: {deaths}\nRecovered: {recovered}\nActive Cases: {active}"
                await context.channel.send(message)
            else:
                await context.channel.send("I'm having trouble retrieving the COVID-19 data. Please try again later.")
        except Exception as e:
            await context.channel.send("Oops! An error occurred while retrieving the COVID-19 data. Please try again later.")
            with open('traceback.txt', 'a') as f:
                f.write(str(e))

async def mal_search(context, *args):
    if len(args) == 0:
        await context.channel.send(f"Um, you didn't specify a search query. You said: {' '.join(context.content.split()[1:])}")
    else:
        query_type = "anime"
        if len(args) > 1 and args[0].lower() in ['anime', 'manga', 'character']:
            query_type = args[0].lower()
            args = args[1:]
        query = " ".join(args).title()
        url = f"https://kitsu.io/api/edge/{query_type}?filter[text]={query}"
        print(f"Sending request to {url}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if len(data['data']) > 0:
                    result = data['data'][0]
                    if query_type == 'anime' or query_type == 'manga':
                        title = result['attributes']['canonicalTitle']
                        url = result['links']['self'].replace('api/edge/', '')
                        image_url = result['attributes']['posterImage']['original']
                        type = result['type']
                        episodes = result['attributes']['episodeCount'] if query_type == 'anime' else result['attributes']['chapterCount']
                        message = f"**{title}**\nType: {type}\nEpisodes/Volumes: {episodes}\nURL: {url}\nImage: {image_url}"
                        await context.channel.send(message)
                    else:
                        name = result['attributes']['canonicalName']
                        url = result['links']['self'].replace('api/edge/', '')
                        image_url = result['attributes']['image']['original']
                        message = f"**{name}**\nURL: {url}\nImage: {image_url}"
                        await context.channel.send(message)

                else:
                    await context.channel.send("Sorry, I couldn't find any results.")
            else:
                await context.channel.send("I'm having trouble retrieving the search results. Please try again later.")
        except Exception as e:
            await context.channel.send("Oops! An error occurred while retrieving the search results. Please try again later.")
            with open('traceback.txt', 'a') as f:
                f.write(str(e))