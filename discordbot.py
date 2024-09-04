#discordbot.py

import os
import random

import discord
from dotenv import load_dotenv

import base64
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps
from PIL import ImageFont
#import urllib.request
from io import BytesIO
#import cv2

def gptwrap(url,img):
        # OpenAI API Key
    api_key = "OPENAI_KEY"

# Function to encode the image
    def encode_image(image_path):
      with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

# "Translate the Japanese text in this image to English."

# Translate the Japanese text in this image to English. Place each section of translated English text in quotes "like this" and indicate the location of each section of text in the image using the terms "top", "middle", "bottom", "left", "right".

    payload = {
      "model": "gpt-4o",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": 'Translate the Japanese text in this image to English. Place each section of translated English text in quotes, and only do this for the English translation. Indicate the location of each section of text in the image using the terms "top", "middle", "bottom", "left", "right".'
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"{url}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())
#print(response.json()['choices'][0]['message'])
    s = response.json()['choices'][0]['message']['content']
    print(s)
#print(response.json()['choices'][0])
    l = s.split('"')[1::2]
    for quote in l:
      print(quote)
    
    #image_path, _ = urllib.request.urlretrieve(url)
    #img = Image.open(image_path)
    y = img.size[1]
    img = ImageOps.pad(img, (img.size[0],y+30*len(l)), color=(255, 255, 255), centering=(0,0))
    myFont = ImageFont.truetype('Arial.ttf', 15)

# Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)
 
# Add Text to an image
    for i in range(len(l)):
        I1.text((0, y+30*i), l[i], font=myFont, fill=(0, 0, 0))
 
# Save the edited image
    img.save("output.png")
    return

load_dotenv()
# Discord API Key
tkn = 'DISCORD_KEY' 
TOKEN = os.getenv(tkn)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f'{message.content}')
    if message.attachments and message.attachments[0].content_type.startswith('image'):
        if message.content.startswith('!t'):
            await message.channel.send('generating...')
            content = await message.attachments[0].read()
            im = Image.open(BytesIO(content))
            gptwrap(message.attachments[0].url,im)
            postpic = discord.File('output.png')
            await message.channel.send(file=postpic)
        elif message.content.startswith('!gray'):
            content = await message.attachments[0].read()
            im = Image.open(BytesIO(content))
            gray = ImageOps.grayscale(im)
            gray.save("output.png")
            postpic = discord.File('output.png')
            await message.channel.send(file=postpic)
            #print('test')
        elif message.content.startswith('!pca'):
            
            return
        return

client.run(tkn)