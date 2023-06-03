import requests
import json
import discord
import io
import config

async def show_image(message):
    # Get the search query from the message content
    query = message.content.split(' ', 2)[-1]

    # Make a GET request to the Unsplash API
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={config.UNSPLASH_API_KEY}"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        await message.channel.send("Oh, I'm sorry. I couldn't find an image for that query.")
        return

    # Parse the JSON response and get the image URL
    data = json.loads(response.text)
    image_url = data['urls']['regular']

    # Send the image as a file in the Discord channel
    image_content = requests.get(image_url).content
    image_file = io.BytesIO(image_content)
    await message.channel.send(file=discord.File(image_file, filename="image.jpg"))