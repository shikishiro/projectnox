import openai
import config

openai.api_key = config.OPENAI_API_KEY

async def chatgpt(personality, message):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=(f"{personality}\nUser: {message}\nNox: "),
        temperature=0.5,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0.5,
    )
    bot_response = response["choices"][0]["text"]
    return bot_response