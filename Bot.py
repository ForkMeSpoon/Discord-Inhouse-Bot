#written by seymo5#2087

from logging import captureWarnings
from types import NoneType
import discord
from discord.ext import tasks
import random

main_channel = 0 #what channel the bot will listen and send commands in (is an integer)

#get api keys from external document
text_file= open("API_KEYS.txt","r")
api_keys = text_file.read()
api_keys = api_keys.split(",")
text_file.close()

current_queue = []

timeout = 0

client = discord.Client()

@client.event
async def on_ready():
    #send message when bot has finished startup
    print(f'{client.user} has connected to Discord!')

    await send_discord_message(f'Im ready to RUMBLE!')

@client.event
async def on_message(message):

    global current_queue
    global timeout

    if message.author == client.user:
        return #ignore message if sent by bot

    if message.channel.id != main_channel:
        return #wrong channel bucko

    msg = message.content.lower()


    if msg == '$queue':
        #await send_discord_message("There are currently " + str(len(current_queue)) + " players in queue")
        tempstr = f"There are currently "  + str(len(current_queue)) +  f" players in queue \n Players in queue: \n       "
        for i in current_queue:
            temp_player = await client.fetch_user(i)
            tempstr = tempstr + str(temp_player.name) + '\n       '
        await send_discord_message(tempstr)


    if msg == '$join':
        #player would like to join queue

        if message.author.id in current_queue:
            #player is already in que, so dont let them join a second time
            await send_discord_message(f"You are already in queue silly") 
            return

        #add player to queue
        current_queue.append(message.author.id)

        timeout = 0 #queue changes so reset timeout timer

        await send_discord_message(f"You have joined the queue")
        
        if len(current_queue) == 10:
            #there are 10 players in queue so start a game

            #start a game

            team_blue, team_red = generate_teams(current_queue)

            await send_discord_message(f"Game 69 begins \n \n Blue team: \n <@{team_blue[0]}> \n <@{team_blue[1]}> \n <@{team_blue[2]}> \n <@{team_blue[3]}> \n <@{team_blue[4]}> \n \n Red team: \n <@{team_red[0]}> \n <@{team_red[1]}> \n <@{team_red[2]}> \n <@{team_red[3]}> \n <@{team_red[4]}>")

            current_queue = [] #reset queue as players have been placed in game. there will only ever be a max of 10 players in queue
            return


        #there is not enough players in queue therefore show how many players are in queue
        await send_discord_message("There are currently " + str(len(current_queue)) + " players in queue")

        return


    if msg == "$leave":
            
        if message.author.id in current_queue:
            #player is indeed in the queue, so remove them
            current_queue.remove(message.author.id)
            await send_discord_message("You have abandoned the real battle")
            await send_discord_message("There are currently " + str(len(current_queue)) + " players in queue")
            return
            
        await send_discord_message("You have to join the queue to leave it")
        return


def generate_teams(players):
    random.shuffle(players)
    return players[0:5], players[5:10]
        
async def send_discord_message(message):
    
    channel = client.get_channel(main_channel)
    
    await channel.send(message)


#bit jank but y'know. it works
@tasks.loop(seconds=60)
async def queue_timeout():

    global current_queue
    global timeout
    timeout += 1

    if timeout >= 60:
        timeout = 0
        if current_queue != []: #check queue is not empty to stop random spam messages
            #if queue has not been changed for an hour then clear it
            current_queue = []
            await send_discord_message("Queue has been emptied due to inactivity")
            
    return



client.run(api_keys[0])
queue_timeout.start() #start the timeout loop
