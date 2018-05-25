from map import *
from tile import *
from screen import *
from block import *
from entity import *
from renderer import *
import numpy
import pygame
import os
"""
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if s.map.y > 0:
                    if s.map.matrix[s.map.y-1][s.map.x] != 1:
                        s.map.move(s.map.x, (s.map.y-1))
                        print(s.map.x, s.map.y)
            elif event.key == pygame.K_LEFT:
                if s.map.x > 0:
                    if s.map.matrix[s.map.y][s.map.x-1] != 1:
                        s.map.move((s.map.x-1), s.map.y)
                        print(s.map.x, s.map.y)
            elif event.key == pygame.K_RIGHT:
                if s.map.x < (s.map.mx-1):
                    if s.map.matrix[s.map.y][s.map.x+1] != 1:
                        s.map.move((s.map.x+1), s.map.y)
                        print(s.map.x, s.map.y)
            elif event.key == pygame.K_DOWN:
                if s.map.y < (s.map.my-1):
                    if s.map.matrix[s.map.y+1][s.map.x] != 1:
                        s.map.move(s.map.x, (s.map.y+1))
                        print(s.map.x, s.map.y)
            s.render()
            pygame.display.flip()
        elif event.type == pygame.QUIT:
            pygame.quit()
        else:
            s.render()
            pygame.display.flip()
"""

class Renderer:

    def __init__(self, view):
        self.view = view

    def init_screen(self, map):
        self.screen = Screen(self.view, map)

    def run_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.screen.map.y > 0:
                            if self.screen.map.matrix[self.screen.map.y-1][self.screen.map.x] != 1:
                                self.screen.map.move(self.screen.map.x, (self.screen.map.y-1))
                    elif event.key == pygame.K_LEFT:
                        if self.screen.map.x > 0:
                            if self.screen.map.matrix[self.screen.map.y][self.screen.map.x-1] != 1:
                                self.screen.map.move((self.screen.map.x-1), self.screen.map.y)
                    elif event.key == pygame.K_RIGHT:
                        if self.screen.map.x < (self.screen.map.mx-1):
                            if self.screen.map.matrix[self.screen.map.y][self.screen.map.x+1] != 1:
                                self.screen.map.move((self.screen.map.x+1), self.screen.map.y)
                    elif event.key == pygame.K_DOWN:
                        if self.screen.map.y < (self.screen.map.my-1):
                            if self.screen.map.matrix[self.screen.map.y+1][self.screen.map.x] != 1:
                                self.screen.map.move(self.screen.map.x, (self.screen.map.y+1))
                    self.screen.render()
                    pygame.display.flip()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                else:
                    self.screen.render()
                    pygame.display.flip()

matrix = numpy.array([
    [1, 1, 1, 1, 1],
    [1, 2, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 1],
    [1, 0, 1],
    [1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1]
])



m = Map(matrix.tolist())
m.x += 1
m.y += 1

renderer = Renderer(2)
renderer.init_screen(m)
renderer.run_screen()
