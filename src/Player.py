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

    CONSTANT_SPEED = 10 * 60

    MAX_SANITY = 100


    def __init__(self, game_data):

        self.animation_names = ['stand_up', 'stand_down', 'stand_left', 'stand_right',
                            'walking_left', 'walking_right', 'walking_down', 'walking_up', 'playing']

        GameObject.__init__(self, "player", game_data)
        self.state = self.STATE_LEFT
        self._layer = 2
        self.tags.append("player")

        self.dest = pygame.Rect(1500, 500, 0, 0)
        self.scale = 0.75
        self.speed = self.CONSTANT_SPEED
        self.run = False
        self.move_rel = Point(0, 0)

        self.sanity = self.MAX_SANITY

    def movement(self):

        old_pos = Point(self.dest.topleft)

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            self.run = True
            self.speed = self.CONSTANT_SPEED * 1.5 * self.system.delta_time / 1000
        else:
            self.run = False
            self.speed = self.CONSTANT_SPEED * self.system.delta_time / 1000

        move = False

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            move = True
            self.dest[0] -= self.speed
            if self.state in (self.STATE_LEFT, self.STATE_WALKING_LEFT):
                self.state = self.STATE_WALKING_LEFT
                self.current_animation_name = "walking_left"
            else:
                self.state = self.STATE_LEFT
                self.current_animation_name = "stand_left"

        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            move = True
            self.dest[0] += self.speed
            if self.state in (self.STATE_RIGHT, self.STATE_WALKING_RIGHT):
                self.state = self.STATE_WALKING_RIGHT
                self.current_animation_name = "walking_right"
            else:
                self.state = self.STATE_RIGHT
                self.current_animation_name = "stand_right"

        if pygame.key.get_pressed()[pygame.K_UP]:
            move = True
            self.dest[1] -= self.speed
            if self.state in  (self.STATE_UP, self.STATE_WALKING_UP):
                self.state = self.STATE_WALKING_UP
                self.current_animation_name = "walking_up"
            else:
                self.state = self.STATE_UP
                self.current_animation_name = "stand_up"

        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            move = True
            self.dest[1] += self.speed
            if self.state is self.STATE_DOWN or self.STATE_WALKING_DOWN:
                self.state = self.STATE_WALKING_DOWN
                self.current_animation_name = "walking_down"
            else:
                self.state = self.STATE_DOWN
                self.current_animation_name = "stand_down"

        if not move:
            if self.state is self.STATE_WALKING_LEFT:
                self.current_animation_name = "stand_left"
                self.state = self.STATE_LEFT
            elif self.state is self.STATE_WALKING_DOWN:
                self.state = self.STATE_DOWN
                self.current_animation_name = "stand_down"
            elif self.state is self.STATE_WALKING_RIGHT:
                self.current_animation_name = "stand_right"
                self.state = self.STATE_RIGHT
            elif self.state is self.STATE_WALKING_UP:
                self.current_animation_name = "stand_up"
                self.state = self.STATE_UP

        self.move_rel = self.dest.topleft - old_pos

    def update(self):

        self.movement()
        GameObject.update(self)

    def on_collision(self, other_go):
        # precisa rechecar a colisão se houve alguma modificação
        if other_go.rigid and other_go.dest.colliderect(self.rect):
            clip = other_go.dest.clip(self.rect)
            self.move_rel = -self.move_rel.int()
            self.dest.topleft += self.move_rel
