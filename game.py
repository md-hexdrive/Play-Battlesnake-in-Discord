# interact with a discord Battlesnake game

from board import Board, Pos

class Player:

    def __init__(self, player_name, snake):
        self.player_name = player_name
        self.snake = snake

        self.head_symbol = "snake_head_bendr"
        self.body_symbol = "red_square"
        self.tail_symbol = "snake_tail_skinny"
    
#TODO: the current head-tail printing strategy needs to be updated when we move to the Battlesnake-Official discord server  
skinny_tails = {
    "up": "<:snake_tail_skinny_up:814954971630927903> ",
    "down": "<:snake_tail_skinny_down:814954948927291424> ",
    "left": "<:snake_tail_skinny_left:814955316633403413> ",
    "right": "<:snake_tail_skinny_right:814955295255953470> "
}

bendr_heads = {
    "up": "<:snake_head_bendr_up:814951268995956809> ",
    "down": "<:snake_head_bendr_down:814952093659562024> ",
    "left": "<:snake_head_bendr_left:814952020476952656> ",
    "right": "<:snake_head_bendr_right:814952048252420197> "
}


class Game:
    def __init__(self, message):
        
        # store the channel this game is being played on
        self.channel = message.channel
        
        # the turn we are currently at
        self.turn = 0

        self.board = Board(10,9)
        self.players = []

        self.players.append(Player(message.author, self.board.snake1))
        
    
    def is_move(self, message):
        '''Does this message signify a valid move command?'''
        return self.channel == message.channel and message.content.startswith('$') and message.content.strip('$') in ["start", "play", "up", "down", "left", "right", "end"]

    def make_move(self, direction):
        '''
        Make a move in the given direction
        '''
        self.last_move = direction
        self.board.snake1.move(direction)
        self.board.update()
        self.turn += 1
    
    def __str__(self):
        '''get and return the board's (emoji) string representation'''

        response=""

        if self.turn == 0:
            response += "Starting a new game"
        elif self.board.is_game_over():
            response += f"Game Over, turn {self.turn}"
        else:
            response += f" \n \nGame at turn {self.turn}"
        
        response += "\n"

        if not self.board.is_game_over():
            snake = self.board.snake1
            self.board[snake.tail] = skinny_tails[snake.tail_dir()]
            self.board[snake.head] = bendr_heads[snake.last_move]
            
            #f":snake_head_bendr_{snake.last_move}: "

        for j in range(self.board.height):
            for i in range(self.board.width):
                response += self.board[Pos(i, self.board.height-j-1)]
            response += "\n"
        
        return response
        

        