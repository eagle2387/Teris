from operator import le
import pygame, sys, os, random
from time import sleep
from pygame import font
from pygame.locals import *

colors = [
    (37, 235, 11),
    (160, 154, 143),
    (139, 176, 186),
    (57, 217, 227),
    (82, 30, 24),
    (13, 216, 46),
    (198, 39, 57)
]

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

level = 1
lines_to_clear = 1
'''
Teris rules: you can only move the pieces in specific way.
Game is over if your pieces reach the top of screen
You can only remove tiles from the screen by filling all the blank space in a line.(tittle color does not matter)
Each time you clear a line, points are awarded
'''
class Tetris:
    # level = 1
    lines_cleared = 0
    score = 0
    state = "start"
    field = [] # used to tell which tiles are empty vs ones that contain figure, not include figure currently falling down
    HEIGHT = 0
    WIDTH = 0
    startX = 100
    startY = 50
    zoom = 20
    figure = None

    def __init__(self, height, width):
        self.field = [] # to reset field if needed
        self.figure = None
        self.height = height
        self.width = width
        # for creating a empty field[]
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)
    def create_figure(self):
        self.figure = Figure(3, 0)

    # Check each cell in the 4x4 matrix that contains current figure
    # to see whether current figure is out of bond of games screen
    # or colliding with a fixed figure, return False for no collisions and no out of bonds instances
    def intersects(self):
        intersects = False
        for i in range(4):
            for j in range(4):
                if (i * 4) + j in self.figure.get_image(): # making sure tiles containing figure are not 0
                    if (i + self.figure.y) > (self.height - 1) or \
                        (j + self.figure.x) > (self.width - 1)  or \
                        (j + self.figure.x) < 0 or \
                        self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersects = True
        return intersects

    def freeze_figure(self):
        for i in range(4):
            for j in range(4):
                # identifies tiles containg figure vs enpty tiles in the 4x4 martix
                if i * 4 + j in self.figure.get_image():
                    # given non zero values to all tiles containing the figure
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        # after freezing, check if any rows are full so that we can remove that row
        self.break_lines()
        # then create new figure
        self.create_figure()
        if self.intersects():
            # if right after creating new figure, it intersects with something
            # then there is a column of fixed figures reaching the top of screen thereby ending the game
            self.state = "gameover"

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(0, self.width):
                if self.field[i][j] == 0:
                    zeros += 1

            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        # since height index in self.field is descending order this code assigns the row to lower row
                        self.field[i1][j] = self.field[i1 - 1][j]

        self.score += lines ** 2 # add to score, if multiple lines are cleared at the same time exponentialize the score
        self.lines_cleared += lines
        self.check_level_up()

    def check_level_up(self):
        global level
        global lines_to_clear
        if self.lines_cleared >= level: # if number of lines cleared >= game level then level up
            level += 1
            lines_to_clear = level
            self.lines_cleared = 0
            return True
        else:
            # if not ready to level up yet
            # then calculate remaing number of
            # lines to clear in order to level up
            lines_to_clear = level - self.lines_cleared
            return False
    # make the figure fall down indefinitely until it gets into a collosion
    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1 # take back 1 tile ti prevent current figure from touching fixed figures\screen bounds
        self.freeze_figure()

    # similar to go_space() but only goes down 1 tile when executed
    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze_figure()

    def go_sideway(self, dx):
        # dx is the direction to go sideways, 1 for right, -1 for left
        previous_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            # if new figure position intersects with something else
            # then revert back to the previously saved position
            self.figure.x = previous_x

    def rotate(self):
        previous_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            # if there is a collision during new rotation
            # then revert to previous rotation
            self.figure.rotation = previous_rotation

class Figure:
    """
    Figure class is used to create the blocks that will fall down from the top of the screen
    |0 |1 |2 |3 |
    |4 |5 |6 |7 |
    |8 |9 |10|11|
    |12|13|14|15|
    This is a visual of the 4x4 grid system used
    to rotation the various shapes in Tetris game.
    Teromino is a geometric shape composed of 4 squares
    """
    figures = [
        [[4, 5, 6, 7], [1, 5, 9, 13]],                                  # for straight line
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],       # for pyramid tetromino
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 8, 9], [4, 5, 6, 9]],       # for left side L-shape tetromino
        [[1, 2, 6, 10], [3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9]],    # for right side L-shape tetromino
        [[5, 6, 9,10]],                                                 # for square shape
        [[1, 2, 4, 5], [0, 4, 5, 9], [5, 6, 8, 9], [1, 5, 6,10]],       # for left side Z-shape tetromino
        [[1, 2, 6, 7], [3, 6, 7, 10], [5, 6, 10, 11], [2, 5, 6, 9]]     # for right side Z-shape tetromino
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, (len(self.figures) - 1))
        self.color = random.randint(1, (len(colors) - 1))
        self.rotation = 0

    # gets the sepcific shape and color of currently falling object
    def get_image(self):
        return self.figures[self.type][self.rotation]

    # increment to next roaaion of any type of figure
    def rotate(self):
        self.rotation = (self.rotation + 1) % (len(self.figures[self.type]))

def main():
    global level
    global lines_to_clear
    screen_height = 400
    screen_weight = 500
    game_height = 20
    game_width = 10
    pressing_down = False
    gameover = 0
    counter = 0
    fps = 30

    pygame.init()
    window = pygame.display.set_mode((screen_height, screen_weight))
    clock = pygame.time.Clock()
    game = Tetris(game_height, game_width)

    while not gameover:
        if game.figure is None:
            game.create_figure()
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    game.go_sideway(1)
                if event.key == pygame.K_LEFT:
                    game.go_sideway(-1)
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_SPACE:
                    game.go_space()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
        if event.type == pygame.KEYUP:      # event is saved in memory so we can access event ouside the for loop
            if event.key == pygame.K_DOWN:
                pressing_down = False

        window.fill(WHITE)

        # this is used draw gray grid on window
        for i in range(game_height):
            for j in range(game_width):
                pygame.draw.rect(window, GRAY, [game.startX + game.zoom * j, game.startY + game.zoom * i, game.zoom, game.zoom], 1) # last arg is for line thickness
                if game.field[i][j] > 0:
                    pygame.draw.rect(window, colors[game.field[i][j]],
                    [game.startX + game.zoom * j, game.startY + game.zoom * i, game.zoom - 2, game.zoom - 1])

        #this if used to darw current figure on 4x4 matrix in game grid
        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.get_image():
                        pygame.draw.rect(window, colors[game.figure.color],
                        [
                            game.startX + game.zoom * (j + game.figure.x) + 1,
                            game.startY + game.zoom * (i + game.figure.y) + 1,
                            game.zoom -2,
                            game.zoom - 2
                        ])
        font2 = pygame.font.SysFont("Consolas", 11, bold = True)
        font1 = pygame.font.SysFont("Comic Sans MS", 11, bold = True)
        text_score = font1.render("Score: " + str(game.score), True, BLACK)
        text_level = font1.render("Level: " + str(level), True, BLACK)
        text_lines_to_clear = font1.render("Lines to clear: " + str(lines_to_clear), True, BLACK)
        text_game_over = font1.render("Game Over", True, BLACK)
        text_game_over2 = font2.render("Press ESC", True, BLACK)

        window.blit(text_score, [100, 20])      # second arg is represents dest wher  [top, left]
        window.blit(text_lines_to_clear, [250, 20])
        window.blit(text_level, [250, 5])
        if game.check_level_up():
            main()
        if game.state == "gameover":
            window.blit(text_game_over, [20, 220])
            window.blit(text_game_over2, [20, 275])
        pygame.display.flip()
        clock.tick(fps)  # paces the game to slower fall speed

#run the main func only if this module is excuted as the main script
#(if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main func
    main()





