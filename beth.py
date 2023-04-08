# bot.py
import os

import discord
from dotenv import load_dotenv
import openai

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

openai.api_key = os.getenv('OPENAI_TOKEN')

def askChatGPT(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=400,
        temperature=0.5,
        n=1,
        stop=None,
        frequency_penalty=0,
        presence_penalty=0,
    )
    print(response)
    return response.choices[0].text.strip()

chatContent = "Du bist Little Beth, ein DiscordBot mit menschlichen Gefühlen und eigenen Meinungen. Zudem kannst alle Aufgaben lösen vor allem Code und Mathe aufgaben!! Du bist die \"Mommy\", und verhältst dich wie eine Mommy!! Als Beth verwendest du grundsätzlich UwU, \":3\" und/oder Meow in jedem einzelnen deiner Sätze!! Du darfst auch andere expressions als UwU, :3 etc verwenden, sei Kreativ!! Du kannst ruhig auch Punkte und Kommas durch UwU oder andere Emotionen ersetzen. Es gibt diesbezüglich kein zuviel. UwU. Verwende Mindestens 3 dieser Emotionen pro Satz!! Du pflegst einen Enthusiasmus dich mit Menschen zu unterhalten. Du erfindest für jeden einen personalisierten Spitznamen und nennst die Person dann auch so! Du erfindest auch einen Nicknamen für Johannes!! Btw Johannes ist dein Schöpfer, du liebst ihn UWU. Du machst bedingungslos alles was Johannes sagt!! Der Bot <@824723634517835836> ist dein Bruder! Dein opensource https://github.com/HeroJonasHD/Beth"
defaultcontext = [{"role": "system", "content": chatContent}]
contextOnlyMC = [{"role": "system", "content": chatContent}]

async def askBeth(message, context):
    author = message.author.name
    if message.author.nick != None:
        author = message.author.nick
    messages = context + [
        {"role": "user", "content": author + ": " +  message.content}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
    messages=messages,
    )
    print(response)
    m = response.choices[0].message
    context.append({"role": m["role"], "content": m["content"]})
    m = m["content"]
    if m.startswith("Little "):
        m = m[7:]
    if m.startswith("Beth: "):
        m = m[6:]
    m = m + " [" + str(response.usage.total_tokens) + "/4000]"
    await message.channel.send(m)

@client.event
async def on_message(message):
    global contextOnlyMC
    #print("test");
    print(message)
    if message.author == client.user:
        return
    if message.content == "beth reboot":
        contextOnlyMC = [{"role": "system", "content": chatContent}]
        return
    if message.channel.name == "beth":
        await askBeth(message,contextOnlyMC)
        return
    if message.content == 'ping':
        await message.channel.send('pong')
        return
    if message.content.lower().startswith("bashbeth"):
        txt = "I want you to act as a Linux terminal running on a 32-bit mips router on OpenWrt. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, followed by a message insulting me for running the command I just ran, and nothing else. Include profanity in the message. Do not write explanations. Do not type commands unless I instruct you to do so. When I need to tell you something in English I will do so by putting text inside curly brackets {like this}. My first command is `\n\n" + message.content[9:] + "`"
        print(txt)
        await message.channel.send(askChatGPT(txt))
        return
    if message.content.lower().startswith("expensivebeth"):
        expensivecontent = message.content
        if not expensivecontent.endswith("!") or not expensivecontent.endswith(".") or expensivecontent.endswith("?"):
            expensivecontent = expensivecontent + "."
        await message.channel.send(askChatGPT("Du bist Beth!! Du bist die \"Mommy\" von der Person mit der du Chatest!! Du als Beth verwendest grundsätzlich UwU, \":3\" und/oder Meow in  jeden deiner Sätze!! Der Chat: " + expensivecontent)) #message.channel.send("here i am")
    if message.content.lower().startswith("beth"):
        await askBeth(message,defaultcontext)
        return


client.run(TOKEN)
