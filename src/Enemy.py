import pygame
from random import random, choice
from engine import Scene, GameObject, Point, Physics

class Enemy(GameObject):

    STATE_LEFT = 1
    STATE_RIGHT = 2
    STATE_UP = 3
    STATE_DOWN = 4

    AGGRO_VISION = 300
    AGGRO_AUDITION = 600

    def __init__(self, game_data, pos):
        self.animation_names = ['up', 'down', 'left', 'right']
        GameObject.__init__(self, 'monster', game_data)

        self._layer = 2
        self.current_animation_name = 'down'

        self.dest = pygame.Rect(pos[0], pos[1], 0, 0)
        self.scale = 3

    def update(self):
        pass