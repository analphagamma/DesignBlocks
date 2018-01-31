from turtle import *
import json
import os.path
from math import sqrt
from random import randint
from time import sleep
from itertools import product


COLORS = ['blue', 'white', 'red', 'yellow',
          'blue-yellow', 'red-white']

board_layout = {}


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

        ht()
        home()
        
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
        penup()
        goto(self.location[0])
        pendown()
        seth(0)
        ht()

    def draw_tile(self):

        def draw_square_filled(self, col):
            '''draws a square filled with solid color'''

            color(col)
            begin_fill()
            seth(0)
            for i in range(4):
                fd(board.scale)
                rt(90)
            end_fill()

        def draw_square_split(self, col1, col2):
            '''draws 2 triangles forming a square filled with the 2 given colors'''

            # if the orientation in the mirror image of the default
            # swap the colors
            if self.orientation in [1, 3]:
                col1, col2 = col2, col1
            # two different orientations
            if self.orientation in [0, 1]:
                color(col1)
                begin_fill()
                seth(0)
                fd(board.scale)
                rt(135)
                fd(sqrt(2*(board.scale**2)))
                rt(135)
                fd(board.scale)
                end_fill()

                rt(90)
                fd(board.scale)

                color(col2)
                begin_fill()
                rt(90)
                fd(board.scale)
                rt(90)
                fd(board.scale)
                end_fill()
            else:
                color(col1)
                begin_fill()
                seth(90)
                fd(board.scale)
                lt(90)
                fd(board.scale)
                lt(135)
                fd(sqrt(2*(board.scale**2)))
                end_fill()

                rt(135)
                color(col2)
                begin_fill()
                fd(board.scale)
                rt(90)
                fd(board.scale)
                end_fill()
                
        if self.orientation == None:
            draw_square_filled(self, self.fill_color)
        else:
            draw_square_split(self, self.fill_color[0], self.fill_color[1])



class Player(object):
    '''This class contains all player behaviour'''

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


class Game(object):
    '''Game engine'''

    def start_game(self):
        ht()
        welcome_lines = ['Welcome to Blocks!',
                         'a game of creativity',
                         'no highscores, no competition',
                         'just play :)']
        for line in welcome_lines:
            clear()
            write(line, align='center', font=('Helvetica', 20, 'bold'))
            sleep(2)

        return self.play_game()

    def play_game(self):
        '''main game sequence
           sets up board and listens to mouse and keyboard actions'''
        
        board.setup_board()

        # defining mouse and keyboard actions
        onscreenclick(player.left_click, 1)
        onscreenclick(player.middle_click, 2)
        onscreenclick(player.right_click, 3)
        
        onkeypress(board.setup_board, 'r')
        listen()

    def save_board(self):
        '''Asks for filename
           if empty string entered -> no save
           if filename already exists -> asks again
           else -> saves file in json format'''
           
        filename = textinput('Save board?', 'To save please enter name.')
        while True:
            if filename in ['', None]:
                print('Not saving.')
                return
        
            if not os.path.isfile(filename+'.json'):
                with open(filename+'.json', 'w+') as f: json.dump(board_layout, f)
                print('Board saved.')
                return
            else:
                print('Filename already exists.')
                filename = textinput('Save as...', 'To save please enter name.\nTo exit without saving press ENTER.')
                
    def load_board(self):
        '''loads a previously saved board
           //TODO'''

        filename = textinput('Load board?', 'Enter name file name to load or leave empty to start a new board')
        while True:
            if filename in ['', None]:
                print('Not loading.')
                return None
        
            if not os.path.isfile(filename+'.json'):
                with open(filename+'.json', 'r+') as f: board_layout = json.load(f)
                return board_layout
            else:
                print('File doesn\'t exist.')
                filename = textinput('Load board?', 'Enter name file name to load or leave empty to start a new board')


    def play_end(self):
        '''prompts to save the board,
           displays exit message and exits'''

        self.save_board()
        clear()
        penup()
        home()
        color('black')
        ht()
        write('Thank you for playing!', align='center', font=('Helvetica', 20, 'bold'))
        exitonclick()


def main():
    scr.screensize(board.scale*6, board.scale*6)
    scr.setup(width=board.scale*7, height=board.scale*7)
    scr.title('Blocks')
    scr.bgcolor('gray')
    scr.delay(0)

    game.start_game()
    return 'EVENTLOOP'


if __name__ == '__main__':
    scr = Screen()
    mode("logo")
    board = Board(150)
    player = Player()
    game = Game()

    main()
    mainloop()
