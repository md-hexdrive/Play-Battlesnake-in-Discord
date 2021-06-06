# Represent the game board in emojis
import numpy as np
from collections import deque
import random
free_space = ":white_large_square: "
food = ":red_circle: "
snake_head = ":green_square: "
snake_body = ":red_square: "
snake_tail = ""

# hold a list of the board occupants that you can collide with for reference
collidable_objects = [snake_head, snake_body]
width = 7
height = 7

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def up(self):
        new_pos = Pos(self.x, self.y + 1)
        return new_pos
    
    def down(self):
        new_pos = Pos(self.x, self.y - 1)
        return new_pos
    
    def left(self):
        new_pos = Pos(self.x - 1, self.y)
        return new_pos

    def right(self):
        new_pos = Pos(self.x + 1, self.y)
        return new_pos

# get all the moves one could theoretically make from pos    
def all_moves(pos):
    return {
        "up" : pos.up(),
        "down": pos.down(),
        "left": pos.left(),
        "right": pos.right()
    }


class Board:

    def __init__(self, width=7, height=7, start=Pos(1, 1)):
        self.grid = np.zeros((width, height), dtype=object)
        self.width = width
        self.height = height
        self.food = []

        self.start_positions = [Pos(1, 1), Pos(self.width//2, self.height//2), Pos(self.width-2, self.height-2)]

        self.snake1 = Snake(self, random.choice(self.start_positions))

        self.update()

        
    
    def is_game_over(self):
        '''Is this game over?'''
        return not self.snake1.is_alive
        
    def __getitem__(self, position):
        return self.grid[position.x][position.y]
    
    def __setitem__(self, position, value):
        self.grid[position.x][position.y] = value

    def spawn_food(self):
        '''Randomly spawn a new piece of food on the board'''
        while len(self.food) == 0:
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            food_pos = Pos(x, y)
            if not self.is_collision(food_pos):
                self.food.append(food_pos)
                break
                
    
    def update(self):
        self.spawn_food()
        # reset the game grid for this turn
        self.grid.fill(free_space)
        for pos in self.food:
            self[pos] = food
        
        if self.snake1.is_alive:
            for pos in self.snake1.body:
                self[pos] = snake_body
            self[self.snake1.head] = snake_head

    def in_bounds(self, pos):
        return pos.x in range(self.width) and pos.y in range(self.height)

    def is_collision(self, pos):
        '''
        Will moving to this board position result in a collision?
        TODO: account for tail moving out of a given location? (or call this after you remove the last position in your body from you body list)
        '''
        if not self.in_bounds(pos):
            return True
        elif self[pos] in collidable_objects:
            return True
        else:
            return False

    
    




class Snake:

    def __init__(self, board, start):

        self.head = start
        self.length = 3
        self.health = 100
        self.body = deque([start, start, start])
        self.tail = start
        self.board = board
        self.is_alive = True

        # store whether our snake ate food in the last turn and needs to expand on this turn
        self.is_growing = False

        # the move our snake made last
        self.last_move = "up"
    
    def move(self, direction="up"):
        '''
        move this snake in the specified direction
        '''
        start = self.head

        # create a dictionary of all the move names we could make -> to the locations we will end up in if we make that move
        moves = all_moves(start)

        # get the correct move location by indexing into the dictionary
        new_head = moves[direction]
        self.last_move = direction
        
        # move our snake's tail, but store its location
        if not self.is_growing:
            old_tail_pos = self.body.popleft()
            self.tail = self.body[0]
        else:
            self.is_growing = False

        # if moving into this location won't kill us, move our head
        if not self.board.is_collision(new_head):
            self.head = new_head
            self.body.append(new_head)

            # handle food eating (increase length and add to tail)
            if self.board[new_head] == food:
                self.length += 1
                self.is_growing = True
                #self.body.appendleft(old_tail_pos)
                #self.tail = old_tail_pos
                self.health = 100

                for i in range(len(self.board.food)):
                    if self.board.food[i] == new_head:
                        del self.board.food[i]
                        return

        # otherwise, handle snake death    
        else:
            self.is_alive = False

    # grow the snake in length
    def grow(self):
        pass
        
    # return the direction this snake's tail is pointing
    # TODO: fix this, it doesn't work yet
    def tail_dir(self):
        target = self.body[1]

        moves = all_moves(self.tail)

        for name, pos in moves.items():
            if pos == target:
                return name
                
        if self.tail == target:
            target = self.body[2]
        
        

        for name, pos in moves.items():
            if pos == target:
                return name
        
        return "up"





