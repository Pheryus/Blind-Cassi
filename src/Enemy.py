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

    def __init__(self, game_data, pos, state):
        GameObject.__init__(self, None, game_data)

        self.animation_names = ['stand_up', 'stand_down', 'stand_left', 'stand_right',
                            'walking_left', 'walking_right', 'walking_down', 'walking_up']
        self._layer = 2


        self.dest = pygame.rect(pos[0], pos[1], 0, 0)
        self.scale = 0.5
        self.state = state



    def update(self):
        pass