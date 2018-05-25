import pygame
import numpy

class Screen:

    def __init__(self, _range, map):
        self.range = _range
        self.map = map
        self.size = _range+1+_range
        self.screen = pygame.display.set_mode((self.size*30, self.size*30))
        self.mapping = [i for i in range(self.size)]

    def render(self):
        m = self.map.getrows(self.range)
        for y in self.mapping:
            for x in self.mapping:
                if y < 0 or x < 0:
                    pass
                else:
                    if m[y][x] == 1:
                        pygame.draw.rect(self.screen, (140, 0, 255), ((x*30, y*30), (30, 30)))
                    elif m[y][x] == 2:
                        pygame.draw.rect(self.screen, (70, 255, 50), ((x*30, y*30), (30, 30)))
                    elif m[y][x] == 3:
                        pygame.draw.rect(self.screen, (0, 0, 0), ((x*30, y*30), (30, 30)))
                    elif m[y][x] == 0:
                        pygame.draw.rect(self.screen, (255, 255, 255), ((x*30, y*30), (30, 30)))
