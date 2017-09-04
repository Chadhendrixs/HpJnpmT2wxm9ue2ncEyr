import discord
import asyncio
import random
import pickle
import os
import requests
from lxml import html

client = discord.Client() 



@client.event            #Setting up the bot
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("-----")
    

    
    
@client.event    #Awaiting commands
async def on_message(message):
    if message.content.startswith('-help'):    #Help command
        await client.send_message(message.channel, "Thank you for using ChaddyBot! My prefix is - :D\n`-flip` Flips a coin!\n`-d20` Rolls a 20 sided die!\n`-addquote` This command adds a quote to the list!\n`-quote` This selects a random quote from the list! (see -addquote) \n`-hentai` Posts a NSFW image! (Work In Progress)")

    elif message.content.startswith('-flip'):    #Coin flipping command
        flip = random.choice(['Heads', 'Tails'])
        await client.send_message(message.channel, flip)
    elif message.content.startswith('-d20'):    #Rolling a D20 command
        roll20 = random.randint(1, 20)
        await client.send_message(message.channel, roll20)
    elif message.content.startswith('-addquote'):    #Adding a quote to the file quote_file.pk1 (this file will be created if it's not there)
        if not os.path.isfile("quote_file.pk1"):
            quote_list = []
        else:
            with open("quote_file.pk1", "rb") as quote_file:
                quote_list = pickle.load(quote_file)
        quote_list.append(message.content[9:])
        with open("quote_file.pk1" , "wb") as quote_file:
            pickle.dump(quote_list, quote_file)
        await client.send_message(message.channel, "Added!")
    elif message.content.startswith('-quote'):    #Selecting a random quote from quote_file.pk1
        with open("quote_file.pk1", "rb") as quote_file:
            quote_list = pickle.load(quote_file)
        await client.send_message(message.channel, random.choice(quote_list))
        
    elif message.content.startswith('-hentai'):    #NSFW command that pulls a random picture off of e621.net (WIP)
        if message.content == "-hentai":
            message.content = "-hentai human"
        elif message.content != "-hentai":
            message.content = message.content
        page = requests.get('http://e621.net/post?tags=' + message.content[7:])
        tree = html.fromstring(page.content)
        global links
        links = tree.xpath('//a/@href')
        site()
        if time == "timeout":
            await client.send_message(message.channel, "No results found")
        else:
            newpage = "https://e621.net" + randchoice
            page = requests.get(newpage)
            tree = html.fromstring(page.content)
            global newlinks
            newlinks = tree.xpath('//a/@href')
            secondsite()
            if time == 10000:
                print("We kinda have an issue, the bot timed out looking for the image =~=")
            else:
                await client.send_message(message.channel, randchoice)
            

def site():    #Looking for an image on the site to use
    global randchoice
    global time
    randchoice = random.choice(links)
    time = 0
    while 1==1:
        if "/post/show/" in randchoice:
            return
        elif "/post/show/" not in randchoice:
            randchoice = random.choice(links)
            if time == 10000:
                time = "timeout"
                return
            elif time != 10000:
                time = time+1

def secondsite():    #Found the image, loading that site, looking for the actual image not just the page linked to the thumbnail
    global randchoice
    global time
    randchoice = random.choice(newlinks)
    time = 0
    while 1==1:
        if "/static1.e621.net/data/" in randchoice:
            if "http://iqbd.harry.lu/?url=" in randchoice:
                randchoice.replace('http://iqbd.harry.lu/?url=', '')
                return
            elif "https://www.google.com/searchbyimage?image_url=" in randchoice:
                randchoice.replace('https://www.google.com/searchbyimage?image_url=', '')
                return
            elif "http://saucenao.com/search.php?url=" in randchoice:
                randchoice.replace('http://saucenao.com/search.php?url=', '')
                return
            else:
                return
        elif "/static1.e621.net/data/" not in randchoice:
            randchoice = random.choice(newlinks)
            if time == 10000:
                time = "timeout"
                return
            elif time != 10000:
                time = time+1              
        randchoice.replace('http://iqbd.harry.lu/?url=', '')
        randchoice.replace('https://www.google.com/searchbyimage?image_url=', '')
        randchoice.replace('http://saucenao.com/search.php?url=', '')
                
                
                
                
client.run('YOUR TOKEN HERE')
