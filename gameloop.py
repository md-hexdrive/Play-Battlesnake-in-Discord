
async def gameloop(game, client, channel):
    while True:

            await channel.send(str(game))

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
    