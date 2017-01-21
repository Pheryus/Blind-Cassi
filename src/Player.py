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

        self.dest = pygame.Rect(1000, 500, 0, 0)
        self.scale = 0.5
        self.dest = pygame.Rect(1500, 500, 0, 0)
        self.scale = 0.75
        self.speed = self.CONSTANT_SPEED
        self.run = False

        self.sanity = self.MAX_SANITY
        self.last_pos = self.dest.topleft

    def movement(self):
        self.last_pos = self.dest.topleft

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

    def update(self):

        self.movement()
        GameObject.update(self)

    def render(self):
        self.system.draw_geom('box', rect=self.rect, color=(0,0,0))
        GameObject.render(self)

    def on_collision(self, other_go):
        # precisa rechecar a colisão se houve alguma modificação
        if other_go.rigid and other_go.rect.colliderect(self.rect):
            # rect = self.rect
            # clip = other_go.rect.clip(self.rect)
            # # self.move_rel = -self.move_rel.int()
            # # self.dest.topleft += self.move_rel
            # if rect.left == clip.left and self.state == self.STATE_WALKING_LEFT:
            #     self.dest.x += clip.width
            # elif rect.right == clip.right and self.state == self.STATE_WALKING_RIGHT:
            #     self.dest.x -= clip.width
            # elif rect.top == clip.top and self.state == self.STATE_WALKING_UP:
            #     self.dest.y += clip.height
            # elif rect.bottom == clip.bottom and self.state == self.STATE_WALKING_DOWN:
            #     self.dest.y -= clip.height
            #
            # rect = self.rect
            # clip = other_go.rect.clip(self.rect)
            # if rect.left == clip.left and self.state in (self.STATE_WALKING_RIGHT,self.STATE_WALKING_DOWN, self.STATE_WALKING_UP):
            #     self.dest.x += clip.width
            #
            # rect = self.rect
            # clip = other_go.rect.clip(self.rect)
            # if rect.right == clip.right and self.state in (self.STATE_WALKING_LEFT,self.STATE_WALKING_DOWN, self.STATE_WALKING_UP):
            #     self.dest.x -= clip.width
            #
            # rect = self.rect
            # clip = other_go.rect.clip(self.rect)
            # if rect.top == clip.top and self.state in (self.STATE_WALKING_RIGHT,self.STATE_WALKING_LEFT, self.STATE_WALKING_DOWN):
            #     self.dest.y += clip.height
            #
            # rect = self.rect
            # clip = other_go.rect.clip(self.rect)
            # if rect.bottom == clip.bottom and self.state in (self.STATE_WALKING_RIGHT,self.STATE_WALKING_LEFT, self.STATE_WALKING_UP):
            #     self.dest.y -= clip.height
            move_rel = Point(self.dest.topleft) - Point(self.last_pos)
            while other_go.rect.colliderect(self.rect) and move_rel != Point(0, 0):
                if move_rel.x:
                    self.dest.x -= move_rel.x / abs(move_rel.x)
                    move_rel.x += - move_rel.x / abs(move_rel.x)
                if move_rel.y:
                    self.dest.y -= move_rel.y / abs(move_rel.y)
                    move_rel.y += - move_rel.y / abs(move_rel.y)
