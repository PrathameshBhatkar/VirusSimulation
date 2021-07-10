import pygame
from pygame import draw

from Colors import *


class Person:
    def __init__(self, id, cellSize):
        self.id = id
        self.life = 100
        print(self.id[0] * cellSize, self.id[0])
        self.rect = pygame.Rect(self.id[0] * cellSize, self.id[1] * cellSize, cellSize - 0, cellSize - 0)

        self.is_infected = False
        self.was_infected = False
        self.is_recovered = False
        self.is_protected = False
        self.is_dead = False

    def draw(self, win):
        if self.is_infected:
            self.life -= 1

        color = color_normal

        if self.life <= 0:
            self.is_infected = False
            self.was_infected = False
            self.is_recovered = False
            self.is_dead = True

        if self.is_recovered:
            color = color_recovered
        elif self.is_protected:
            color = color_protected

        elif self.is_dead:
            color = color_ded

        elif self.is_infected:
            color = color_infected

        draw.rect(win, color, self.rect)
