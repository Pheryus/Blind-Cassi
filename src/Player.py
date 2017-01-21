import pygame
from random import random, choice
from engine import Scene, GameObject, Point, Physics

class Player(GameObject):

    STATE_LEFT = 1
    STATE_RIGHT = 2
    STATE_UP = 3
    STATE_DOWN = 4
    STATE_WALKING_LEFT = 5
    STATE_WALKING_RIGHT = 6
    STATE_WALKING_UP = 7
    STATE_WALKING_DOWN = 8

    def __init__(self, game_data):

        self.animation_names = ['stand_up', 'stand_down', 'stand_left', 'stand_right',
                            'walking_left', 'walking_right', 'walking_down', 'walking_up']

        GameObject.__init__(self, "player", game_data)
        self.state = self.STATE_LEFT
        self._layer = 2

        self.tags.append("player")

        self.dest = pygame.Rect(500, 500, 0, 0)
        self.scale = 1

    def update(self):

        if self.state is self.STATE_LEFT:
            self.state_left()

    def state_left(self):

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.state = self.STATE_WALKING_LEFT