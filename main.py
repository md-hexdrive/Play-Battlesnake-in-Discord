'''
Application entry point
'''

# imports
import discord

import os
from time import sleep

from board import Pos, Board, Snake, free_space
from game import Game
from gameloop import gameloop

# The client instance
client = discord.Client()

games = {}
@client.event
async def on_ready():
    '''
    Bot login message
    '''
    print('We have logged in as a {0.user}'.format(client))

@client.event
async def on_message(message):


    response = ""
    if message.author == client.user:
        return

    msg = message.content.lower()
    
    print(f"\n\nReceived Message {message.content}, from {message.author}, on channel {message.channel}, on the server {message.guild}")
    
    if msg.startswith('$hello'):
        response = f'Hello {message.author}!'
    
    if msg.startswith('$help'):
        response = '''
Bot Chat Commands:

**$start** or **$play** - Start a new game.
**$end** - Force-stop a game in progress.
**$help** - This help message.

**$up**, **$down**, **$left**, or **$right**: Move the snake up, down, left, or right.

'''

    if msg.startswith('$create'):

        arguments = msg.split() [1:]
        gamemode = "standard"

        width = 10
        height = 9

        for arg in arguments:
            if arg == "constrictor":
                gamemode = "constrictor"
            
            if arg.startswith('width'):
                width = int(arg[-1])
            if arg.startswith('height'):
                height = int(arg[-1])

        response = f'Creating a new Battlesnake game in Discord, with gamemode: {gamemode}, width: {width}, and height: {height} '#{arguments}'

    
    if msg.startswith('$emojis'):
        response = 'Server emojis' + str(message.guild.emojis)

    elif msg.startswith('$smile'):
        response = ':smile:'
    
    if response != "":
        await message.channel.send(response)
    if msg.startswith('$play') or msg.startswith('$start'):
        
        #send_board(message, Board())
        game = Game(message)
        channel = message.channel

        await message.delete()

#        gameloop(game, client, message.channel)
        
        # send the board's status to discord
        boardMessage = await channel.send(str(game))

        # the game loop
        while True:

            await boardMessage.edit(content=str(game))
#            await boardMessage.clear_reactions()
#            await boardMessage.add_reaction("/:smile:")

            if game.board.is_game_over():
                break
                
            #TODO: add timeout for user to return moves
            message = await client.wait_for("message", check=game.is_move)

            #TODO: add proper game termination and detection code
            if message.content == "$end":
                await message.channel.send("Force ending game")
                break
            elif message.content in ["$start", "$play"]:
                await message.channel.send("Warning, you can't play two games in the same channel at the same time, request ignored")
            else:
                game.make_move(message.content.strip("$"))
            
            # delete move commands to keep them from filling up the window
            await message.delete()

            
        
        #await message.channel.send("Game Over")

    elif msg.startswith('$empty_board'):
        response = ""
        count = 0
        for i in range(7):
            for j in range(7):
                count += 1
                response += free_space
            '''
            if count + 7 > 27 :
                await message.channel.send(response)
                response = ""
                count = 0
            '''
            
            response += "\n"
        await message.channel.send(response)
        
async def send_board(message, board):
    response=""
    count=0
    for j in range(board.height):
        for i in range(board.width):
            response+= board.grid[i, board.height-j-1]
        if count + 7 > 27 :
                await message.channel.send(response)
                response = ""
                count = 0
        response += "\n"
    await message.channel.send(response)
    

# Login using Bot Token
client.run(os.getenv('TOKEN'))
