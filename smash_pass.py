import random

async def smash_pass(message):
    channel = message.channel
    attachments = message.attachments
    if not attachments:
        await channel.send('Umm... please attach an image to play Smash or Pass!')
        return

    responses = ['Umm... Smash! :blush:', 'Pass. :sleepy:', 'Ew. :face_vomiting:']
    probabilities = [0.45, 0.45, 0.1]
    response = random.choices(responses, probabilities)[0]
    await channel.send(f'I... I would {response}')