import turtle
from math import sqrt
from random import choice
from time import sleep
from itertools import product


COLORS = ['blue', 'white', 'red', 'yellow',
          'blue-yellow', 'red-white']

ORIENTATIONS = ['up1', 'up2', 'down1', 'down2']

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
        for location in self.locations:
            color = choice(COLORS)
            print(color)
            if len(color.split('-')) == 1:
                orientation = None
            else:
                orientation = choice(ORIENTATIONS)
            print(orientation)
            tile = Tile(location, color.split('-'), orientation)
            tile.draw_tile()


class Tile(object):
    '''This class handles the behaviour of individual tiles'''

    def __init__(self, location, color, orientation):
        self.location = location
        self.color = color
        self.orientation = orientation
        
        print(self.location, self.color, self.orientation) #for testing purposes

        turtle.penup()
        turtle.goto(self.location[0])
        turtle.pendown()
        turtle.seth(0)

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
            draw_square_filled(self, self.color)
        else:
            print("COLOR:", self.color)
            draw_square_split(self, self.color[0], self.color[1])

    def change_color(self, color):
        self.color = color
        self.draw_tile(self)
        print('Changing color')

    def rotate_tile(self):
        print('Rotating tile')


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
            tile = Tile(board.locations[tile_no], 'black', None)
            tile.draw_tile()

    def right_click(self, x, y):
        '''checks whether the click was inside a tile and calls
           the method to rotate the tile.'''
           
        tile_no = self.check_click(x, y)
        if tile_no is not None:
            print('Rotating Tile No.{}'.format(tile_no))
            
    def middle_click(self, x, y):
        '''Takes user to end screen.'''
        
        print('Exiting.')
        game.play_end()


class Game(object):
    '''Game engine'''
    
    def __init__(self):
        pass

    def start_game(self):
        turtle.ht()
        welcome_lines = ['Welcome to Blocks!',
                         'a game of creativity',
                         'no highscores, no competition',
                         'just playing :)']
        for line in welcome_lines:
            turtle.clear()
            turtle.write(line, align='center', font=('Helvetica', 20, 'bold'))
            sleep(2)

        return self.play_game()

    def play_game(self):
        def exit_game(*args):
            self.play_end()
        
        board.setup_board()
        
        turtle.onscreenclick(player.left_click, 1)
        turtle.onscreenclick(player.middle_click, 2)
        turtle.onscreenclick(player.right_click, 3)

    def play_end(self):
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