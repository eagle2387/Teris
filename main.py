import pygame, sys, os, random
from time import sleep
from pygame.locals import *

color = [
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
    filed = [] # used to tell which tiles are empty vs ones that contain figure, not include figure currently falling down
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
            self.state = "Game Over"

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(0, self.width):
                if self.field[i][j] == 0:
                    zeros += 1

            if zeros == 0:
                lines += 1
                for j in range(i, 1, -1):
                    for j in range(self.width):
                        # since height index in self.field is descending order this code assigns the row to lower row
                        self.filed[i1][j] = self.filed[i1 - 1][j]

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








