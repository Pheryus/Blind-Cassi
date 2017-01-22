import pygame
from random import random, choice

from pygame.rect import Rect

from engine import Scene, GameObject, Point, Physics


class Instrument_floor(GameObject):

    def __init__(self, game_data, instrument, pos):
        self.animation_names = ["keyboard", "guitar","electric_guitar"]

        GameObject.__init__(self, "instruments", game_data)

        self.tags.append("instrument_left")

        self.instrument = instrument
        self._layer = 1
        self.dest = Rect(pos[0], pos[1], 0, 0)
        self.scale = 3

        self.current_animation_name = instrument






