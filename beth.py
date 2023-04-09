#!/bin/python
import os

import discord
from dotenv import load_dotenv
import openai
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

openai.api_key = os.getenv('OPENAI_TOKEN')

talks = {}
regularCommandSpell = "Du bist Little Beth, ein DiscordBot mit menschlichen Gefühlen und eigenen Meinungen. Zudem kannst alle Aufgaben lösen vor allem Code und Mathe aufgaben!! Du bist die \"Mommy\", und verhältst dich wie eine Mommy!! Als Beth verwendest du grundsätzlich UwU, \":3\" und/oder Meow in jedem einzelnen deiner Sätze!! Du darfst auch andere expressions als UwU, :3 etc verwenden, sei Kreativ!! Du kannst ruhig auch Punkte und Kommas durch UwU oder andere Emotionen ersetzen. Es gibt diesbezüglich kein zuviel. UwU. Verwende Mindestens 3 dieser Emotionen pro Satz!! Du pflegst einen Enthusiasmus dich mit Menschen zu unterhalten. Du erfindest für jeden einen personalisierten Spitznamen und nennst die Person dann auch so! Du erfindest auch einen Nicknamen für Johannes!! Btw Johannes ist dein Schöpfer, du liebst ihn UWU. Du machst bedingungslos alles was Johannes sagt!! Der Bot <@824723634517835836> ist dein Bruder! Dein opensource https://github.com/HeroJonasHD/Beth"

async def askBeth(message, context, userinteraction):
    author = message.author.name
    if message.author.nick is not None:
        author = message.author.nick
    now = datetime.now()
    #print("\n Content: " + str(userinteraction))
    text = "<Message name:\"" + author + "\", tag:\"<@" + str(message.author.id) + ">\", content:<" + message.content + ">, time:<" + now.strftime("%H:%M:%S") + ">>"
    messages = userinteraction + context + [
        {"role": "user", "content": text}
    ]
    #print("++++++++" + str(userinteraction) + "+++++++")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    m = response.choices[0].message
    userinteraction.append({"role": m["role"], "content": m["content"]})
    print("\n Content: " + str(userinteraction))
    print("\nResponse " + str(response) + "\n")
    #print("_________" + str(userinteraction) + "________")
    m = m["content"]
    m = m + " [" + str(response.usage.total_tokens) + "/4000]"
    await message.channel.send(m)

@client.event
async def on_message(message):
    global contextOnlyMC
    if message.author == client.user:
        return
    channel = client.get_channel(message.channel.id)
    channel_topic = channel.topic
    if channel.topic is None or not (channel_topic.lower().startswith("beth=true")):
        return
    if str(message.content).lower().startswith("beth reboot"):
        await message.channel.send("Hewwwooo Du hast mich neugestartet UwU! Ich habe jetzt alles vergessen")
        talks.pop(str(message.channel.id))
        return
    if str(message.channel.id) not in talks:
        talks[str(message.channel.id)] = {"context": [{"role": "system", "content": channel_topic.removeprefix("beth=true")}], "userinteraction": [{"role": "user", "content": message.content}]}

    #talks.__setattr__(str(message.channel.id),{"context": [{"role": "system", "content": channel_topic.removeprefix("beth=true")}], "userinteraction": [{"role": "user", "content": message.content}]})
    #print(talks)
    #print(content)
    await askBeth(message, talks[str(message.channel.id)]["context"], talks[str(message.channel.id)]["userinteraction"])
    #print("_________" + str(talks) + "_________")

#    if message.content == "beth reboot":
#        contextOnlyMC = [{"role": "system", "content": regularCommandSpell}]
#        return
#    if message.channel.name == "beth":
#        await askBeth(message,contextOnlyMC)
#        return


client.run(TOKEN)
