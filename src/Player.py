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

    STATE_PLAYING_GUITAR = 9
    STATE_PLAYING_ELECTRIC_GUITAR = 10
    STATE_PLAYING_KEYBOARD = 11

    CONSTANT_SPEED = 50

    def __init__(self, game_data):

        self.animation_names = ['stand_up', 'stand_down', 'stand_left', 'stand_right',
                            'walking_left', 'walking_right', 'walking_down', 'walking_up']

        GameObject.__init__(self, "player", game_data)
        self.state = self.STATE_LEFT
        self._layer = 2
        self.tags.append("player")

        self.dest = pygame.Rect(500, 500, 0, 0)
        self.scale = 0.5
        self.speed = self.CONSTANT_SPEED
        self.run = False



    def movement(self):

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self.run = True
            self.speed = self.CONSTANT_SPEED * 1.5
        else:
            self.run = False
            self.speed = self.CONSTANT_SPEED

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.dest[0] -= self.speed
            if self.state is self.STATE_LEFT or self.STATE_WALKING_LEFT:
                self.state = self.STATE_WALKING_LEFT
                self.current_animation_name = "walking_left"
            else:
                self.state = self.STATE_LEFT
                self.current_animation_name = "stand_left"

        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.dest[0] += self.speed
            if self.state is self.STATE_RIGHT or self.STATE_WALKING_RIGHT:
                self.state = self.STATE_WALKING_RIGHT
                self.current_animation_name = "walking_right"
            else:
                self.state = self.STATE_RIGHT
                self.current_animation_name = "stand_right"

        if pygame.key.get_pressed()[pygame.K_UP]:
            self.dest[1] -= self.speed
            if self.state is self.STATE_UP or self.STATE_WALKING_UP:
                self.state = self.STATE_WALKING_UP
                self.current_animation_name = "walking_up"
            else:
                self.state = self.STATE_UP
                self.current_animation_name = "stand_up"

        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            self.dest[1] += self.speed
            if self.state is self.STATE_DOWN or self.STATE_WALKING_DOWN:
                self.state = self.STATE_WALKING_DOWN
                self.current_animation_name = "walking_down"
            else:
                self.state = self.STATE_DOWN
                self.current_animation_name = "stand_down"


    def update(self):

        self.movement()
        GameObject.update(self)
