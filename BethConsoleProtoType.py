# bot.py
import os

from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv('OPENAI_TOKEN')

#def completeWithDavinci(text):
#    response = openai.Completion.create(
#        engine="text-davinci-003",
#        prompt=text,
#        max_tokens=400,
#        temperature=0.5,
#        n=1,
#        stop=None,
#        frequency_penalty=0,
#        presence_penalty=0,
#    )
#    print(response)
#    return response.choices[0].text.strip()


#webcontent = [
#  {"topic": "Python 3", "target": "Beginners", "link": "youtube.com/beginners"},
#  {"topic": "Python 3 OOP", "target": "Advanced", "link": "youtube.com/oop"},
#  {"topic": "FastAPI", "target": "Intermediate", "link": "youtube.com/fastapi"}
#]
#
#content = f"""
#You are a helpful assistant for my website, where you can learn about coding. Don´t suggest other ressources
#like Codecademy etc. Just my own content. Provide the user the link with the best suited video. Here are my videos:
#'{str(webcontent)}.
#Only answer questions regarding coding. Say 'Please ask google' for anything else.
#'"""

content = "Du bist Beth, ein DiscordBot!! Du bist die \"Mommy\" von der Person mit der du Chatest!! Du als Beth verwendest grundsätzlich UwU, \":3\" und/oder Meow in  jeden deiner Sätze!!"

print("Hello! I'm a helpful assistant for providing information about videos on my channel. How can I assist you today?")
context = [{"role": "system", "content": content}]

while True:
  user_input = input("You: ")
  if user_input.lower() in ["bye", "goodbye", "exit"]:
    print("Assistant: Goodbye!")
    break
  else:
    messages = context + [
      {"role": "user", "content": user_input }
    ]
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages,
    )

    message = response.choices[0].message
    context.append({"role": message["role"], "content": message["content"]})
    print("Assistant:", message["content"])