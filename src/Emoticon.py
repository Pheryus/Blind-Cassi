import pygame
from pygame.rect import Rect

from engine import GameObject


class Emoticon(GameObject):

    def __init__(self, game_data, pos):
        #self.animation_names = ['happy', 'angry']

        GameObject.__init__(self, "cerebro", game_data)
        self._layer = 5
        self.dest = Rect(pos[0], pos[1], 0, 0)
        self.scale = 1


        #animar uma vez


