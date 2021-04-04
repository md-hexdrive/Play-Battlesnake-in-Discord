import discord

import os
from time import sleep

from board import Pos, Board, Snake
from game import Game


client = discord.Client()

games = {}
@client.event
async def on_ready():
    print('We have logged in as a {0.user}'.format(client))

@client.event
async def on_message(message):

    response = ""
    if message.author == client.user:
        return

    
    print(f"\n\nReceived Message {message.content}, from {message.author}, on channel {message.channel}, on the server {message.guild}")
    
    if message.content.lower().startswith('$hello'):
        response = 'Hello!\nI :heart: you!'
    
    if message.content.lower().startswith('$emojis'):
        response = 'Server emojis' + str(message.guild.emojis)

    elif message.content.lower().startswith('$smile'):
        response = ':smile:'
    
    if response != "":
        await message.channel.send(response)
    if message.content.lower().startswith('$play') or message.content.lower().startswith('$start'):
        
        #send_board(message, Board())
        game = Game(message)
        
        while True:

            await message.channel.send(str(game))

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

            
        
        #await message.channel.send("Game Over")

    elif message.content.lower().startswith('$empty_board'):
        response = ""
        count = 0
        for i in range(7):
            for j in range(7):
                count += 1
                response += ":white_large_square: "
            if count + 7 > 27 :
                await message.channel.send(response)
                response = ""
                count = 0
            
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
    


client.run(os.getenv('TOKEN'))
