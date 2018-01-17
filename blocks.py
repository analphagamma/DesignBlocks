import turtle
import json
import os.path
from math import sqrt
from random import randint
from time import sleep
from itertools import product


COLORS = ['blue', 'white', 'red', 'yellow',
          'blue-yellow', 'red-white']


board_layout = {0: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None},
                1: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None},
                2: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None},
                3: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None},
                4: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None},
                5: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None},
                6: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None},
                7: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None},
                8: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None},
                9: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None},
                10: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None},
                11: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None},
                12: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None},
                13: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None},
                14: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None},
                15: {'tile_location': '', 'tile_color': 0, 'tile_orientation': None}}

class Board(object):
    '''represents the whole playing field with all the tiles and their
        locations'''
        
    def __init__(self, scale):
        self.scale = scale
        # creating coordinates for tiles
        lower_coord = []
        lower_positions_x = [-self.scale*2, -self.scale, 0, self.scale]
        lower_positions_y = [self.scale *2, self.scale, 0, -self.scale]
        for x, y in product(lower_positions_x, lower_positions_y):
            lower_coord.append((x, y))
        upper_coord = []
        upper_positions_x = [-self.scale, 0, self.scale, self.scale*2]
        upper_positions_y = [self.scale*3, self.scale*2, self.scale, 0]
        for x, y in product(upper_positions_x, upper_positions_y):
            upper_coord.append((x, y))

        self.locations = list(zip(lower_coord, upper_coord))
        
    def setup_board(self):
        '''places the pen in its initial position
           draws the tiles in a 4x4 format filled with random colors'''

        turtle.ht()
        turtle.home()
        turtle.mode("logo")
        for i, location in enumerate(self.locations):
            color_choice = randint(0,5)
            if color_choice in [0,1,2,3]:
                orientation = None
            else:
                orientation = randint(0,3)
            
            tile = Tile(i, location, color_choice, orientation)
            tile.draw_tile()


class Tile(object):
    '''This class handles the behaviour of individual tiles

       tile_id -> int - to identify the tile
       location -> tuple of tuples ((x0, y0), (xn, yn)) - bottom-left and top-right coordinates of tile
       color_code -> int - index of COLORS list
       orientation -> int or None - # 0: up1, 1:up2, 2:down1, 3:down2, None:filled tile'''

    def __init__(self, tile_id, location, color_code, orientation):
        self.tile_id = tile_id
        self.location = location
        self.color_code = color_code
        self.orientation = orientation

        # translating color code to actual color and splitting double colors
        self.fill_color = COLORS[self.color_code].split('-')

        print(self.tile_id, self.location, COLORS[self.color_code], self.orientation) #for testing purposes
        # storing tile attributes in dictionary
        board_layout[self.tile_id] = {'tile_location': self.location, 'tile_color': self.color_code, 'tile_orientation': self.orientation}

        # initialising turtle position
        turtle.penup()
        turtle.goto(self.location[0])
        turtle.pendown()
        turtle.seth(0)
        turtle.ht()

    def draw_tile(self):

        def draw_square_filled(self, col):
            '''draws a square filled with solid color'''

            turtle.color(col)
            turtle.begin_fill()
            turtle.seth(0)
            for i in range(4):
                turtle.fd(board.scale)
                turtle.rt(90)
            turtle.end_fill()

        def draw_square_split(self, col1, col2):
            '''draws 2 triangles forming a square filled with the 2 given colors'''

            # if the orientation in the mirror image of the default
            # swap the colors
            if self.orientation in [1, 3]:
                col1, col2 = col2, col1
            
            turtle.color(col1)
            turtle.begin_fill()
            turtle.seth(0)
            turtle.fd(board.scale)
            turtle.lt(135)
            turtle.fd(sqrt(2*(board.scale ^ board.scale)))
            turtle.lt(135)
            turtle.fd(board.scale)
            turtle.end_fill()

            turtle.rt(90)

            turtle.color(col2)
            turtle.begin_fill()
            turtle.fd(board.scale)
            turtle.rt(90)
            turtle.fd(board.scale)
            turtle.end_fill()

        if self.orientation == None:
            draw_square_filled(self, self.fill_color)
        else:
            draw_square_split(self, self.fill_color[0], self.fill_color[1])



class Player(object):
    '''This class contains all player behaviour'''
    
    def __init__(self):
        pass

    def check_click(self, x, y):
        '''checks whether the click is within the boundary of any tiles
           returns tile number'''

        for loc in board.locations:
            if (x >= loc[0][0] and x <= loc[1][0] and
                y >= loc[0][1] and y <= loc[1][1]):
                return board.locations.index(loc)

        return None
        
    def left_click(self, x, y):
        '''checks whether the click was inside a tile and calls
           the method to change the color.'''
           
        tile_no = self.check_click(x, y)
        if tile_no is not None:
            print('Changing color at Tile No.{}'.format(tile_no))
            # picking next color in list
            new_color = board_layout[tile_no]['tile_color'] + 1
            # to avoid IndexError
            if new_color > 5:
                new_color = 0
            print('NEW COLOR: ', new_color)
            # filled or split
            if new_color in [0,1,2,3]:
                orientation = None
            else:
                orientation = randint(0,3)
            print('ORIENTATION: ', orientation)
            # re-initialise tile
            tile = Tile(tile_no, board.locations[tile_no], new_color, orientation)
            tile.draw_tile()

    def right_click(self, x, y):
        '''checks whether the click was inside a tile and calls
           the method to rotate the tile.'''
           
        tile_no = self.check_click(x, y)
        if tile_no is not None:
            if board_layout[tile_no]['tile_orientation'] == None:
                print('Can\'t rotate filled tile')
                return
            
            print('Rotating Tile No.{}'.format(tile_no))
            color = board_layout[tile_no]['tile_color']
            new_orientation = board_layout[tile_no]['tile_orientation'] + 1
            if new_orientation > 4:
                new_orientation = 0
            print('NEW ORIENTATION ', new_orientation)
            tile = Tile(tile_no, board.locations[tile_no], color, new_orientation)
            tile.draw_tile()
            
    def middle_click(self, x, y):
        '''Takes user to end screen.'''
        
        print('Exiting.')
        game.play_end()

    def save_board(self):
        '''Asks for filename
           if empty string entered -> no save
           if filename already exists -> asks again
           else -> saves file in json format'''
           
        filename = turtle.textinput('Save board?', 'To save please enter name.')
        while True:
            if filename == '':
                print('Not saving.')
                return
        
            if not os.path.isfile(filename+'.json'):
                with open(filename+'.json', 'w+') as f: json.dump(board_layout, f)
                print('Board saved.')
                return
            else:
                print('Filename already exists.')
                filename = turtle.textinput('Save as...', 'To save please enter name.\nTo exit without saving press ENTER.')
                
            

    def load_board(self):
        
        pass


class Game(object):
    '''Game engine'''
    
    def __init__(self):
        pass

    def start_game(self):
        turtle.ht()
        welcome_lines = ['Welcome to Blocks!',
                         'a game of creativity',
                         'no highscores, no competition',
                         'just play :)']
        for line in welcome_lines:
            turtle.clear()
            turtle.write(line, align='center', font=('Helvetica', 20, 'bold'))
            sleep(2)

        return self.play_game()

    def play_game(self):
                
        board.setup_board()

        # defining mouse and keyboard actions
        turtle.onscreenclick(player.left_click, 1)
        turtle.onscreenclick(player.middle_click, 2)
        turtle.onscreenclick(player.right_click, 3)
        
        turtle.onkeypress(board.setup_board, 'r')
        turtle.listen()

    def play_end(self):
        player.save_board()
        turtle.clear()
        turtle.penup()
        turtle.home()
        turtle.color('black')
        turtle.ht()
        turtle.write('Thank you for playing!', align='center', font=('Helvetica', 20, 'bold'))
        turtle.exitonclick()


def main():
    scr.screensize(board.scale*6, board.scale*6)
    scr.setup(width=board.scale*7, height=board.scale*7)
    scr.title('Blocks')
    scr.bgcolor('gray')
    scr.delay(0)

    game.start_game()
    return 'EVENTLOOP'


if __name__ == '__main__':
    scr = turtle.Screen()
    board = Board(100)
    player = Player()
    game = Game()

    main()
    turtle.mainloop()
