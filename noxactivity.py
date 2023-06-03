import discord

async def set_activity(client):
    activity = discord.Activity(type=discord.ActivityType.watching, name="you")
    await client.change_presence(activity=activity)