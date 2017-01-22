import pygame
from random import random, choice

from pygame import Rect, time

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

    STATE_PLAYING = 9

    CONSTANT_SPEED = 10 * 60


    CONTROL = {
        "action" : lambda : pygame.key.get_pressed()[pygame.K_w],
        "change_instrumentL" : pygame.K_q,
        "change_instrumentR" : pygame.K_e,
        "play_song" : pygame.K_s,
        "up" : lambda : pygame.key.get_pressed()[pygame.K_UP],
        "run" : lambda : pygame.key.get_pressed()[pygame.K_LCTRL],
        "down" : lambda : pygame.key.get_pressed()[pygame.K_DOWN],
        "left" : lambda : pygame.key.get_pressed()[pygame.K_LEFT],
        "right" : lambda : pygame.key.get_pressed()[pygame.K_RIGHT]
    }


    def __init__(self, game_data, pos=(0,0)):

        self.animation_names = ['stand_up', 'stand_down', 'stand_left', 'stand_right',
                            'walking_left', 'walking_right', 'walking_down', 'walking_up', 'guitar', 'electric_guitar', 'keyboard']

        GameObject.__init__(self, "hero", game_data)

        self.instrument_index = 2
        self.instruments = [["keyboard", False], ["guitar", False], ["electric_guitar", True]]

        self.time = 0
        self.max_sanity = 100
        self.state = self.STATE_LEFT
        self._layer = 5
        self.tags.append("player")
        self.current_animation_name = 'walking'

        self.instrument_ref = None
        self.instrument_left_ref = None

        self.can_get_item = False

        self.dest = pygame.Rect(pos[0], pos[1], 0, 0)
        self.scale = 1.5
        self.speed = self.CONSTANT_SPEED
        self.run = False

        self.sanity = self.max_sanity
        self.sanity_per_second = 0.015
        self.last_pos = self.dest.topleft

    def get_instrument(self):
        return self.instruments[self.instrument_index]

    def movement(self):

        if self.state == self.STATE_PLAYING:
            self.current_animation_name = self.get_instrument()[0]
            return

        self.last_pos = self.dest.topleft

        if self.CONTROL["run"]():
            self.run = True
            self.speed = self.CONSTANT_SPEED * 1.5 * self.system.delta_time / 1000
        else:
            self.run = False
            self.speed = self.CONSTANT_SPEED * self.system.delta_time / 1000

        move = False

        if self.CONTROL["left"]():
            move = True
            self.dest[0] -= self.speed
            if self.state in (self.STATE_LEFT, self.STATE_WALKING_LEFT):
                self.state = self.STATE_WALKING_LEFT
                self.current_animation_name = "walking_left"
            else:
                self.state = self.STATE_LEFT
                self.current_animation_name = "stand_left"

        elif self.CONTROL["right"]():
            move = True
            self.dest[0] += self.speed
            if self.state in (self.STATE_RIGHT, self.STATE_WALKING_RIGHT):
                self.state = self.STATE_WALKING_RIGHT
                self.current_animation_name = "walking_right"
            else:
                self.state = self.STATE_RIGHT
                self.current_animation_name = "stand_right"

        if self.CONTROL["up"]():
            move = True
            self.dest[1] -= self.speed
            if self.state in  (self.STATE_UP, self.STATE_WALKING_UP):
                self.state = self.STATE_WALKING_UP
                self.current_animation_name = "walking_up"
            else:
                self.state = self.STATE_UP
                self.current_animation_name = "stand_up"

        elif self.CONTROL["down"]():
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

    def check_instrument(self):

        for event in self.system.get_events():
            if event.type == pygame.KEYDOWN:
                if event.key == self.CONTROL["change_instrumentL"]:
                    if self.instruments[(self.instrument_index + 1) % 3][1]:
                        self.instrument_index = (self.instrument_index + 1) % 3

                    elif self.instruments[(self.instrument_index + 2) % 3][1]:
                        self.instrument_index = (self.instrument_index + 2) % 3
                    else:
                        self.system.sounds.play("cancel")

                    self.instrument_ref.current_animation_name = self.instruments[self.instrument_index][0]
                elif event.key == self.CONTROL["change_instrumentR"]:
                    if self.instruments[(self.instrument_index - 1) % 3][1]:
                        self.instrument_index = (self.instrument_index - 1) % 3
                    elif self.instruments[(self.instrument_index - 2 ) % 3][1]:
                        self.instrument_index = (self.instrument_index - 2) % 3
                    else:
                        self.system.sounds.play("cancel")
                    self.instrument_ref.current_animation_name = self.instruments[self.instrument_index][0]


    def check_action_button(self):

        if self.can_get_item and self.CONTROL["action"]():
            for i in self.instruments:
                if i[0] == self.can_get_item.instrument:
                    i[1] = True
                    self.can_get_item.kill()
                    self.system.sounds.play("get_item")
                    self.can_get_item = None
                    break

    def update(self):
        print(self.rect)
        self.regain_sanity()

        self.check_sanity()
        if not self.instrument_ref:
            a = self.scene.get_gos_with_tag("instrument")
            if a:
                self.instrument_ref = a[0]
        else:
            self.check_instrument()

        if not self.instrument_left_ref:
            a = self.scene.get_gos_with_tag("instrument_left")
            if a:
                self.instrument_left_ref = a[0]
        else:
            self.check_action_button()

        self.movement()
        GameObject.update(self)


    def regain_sanity(self):
        if self.sanity + 1 <= self.max_sanity:
            self.sanity += self.sanity_per_second

    def check_sanity(self):
        if self.sanity < 0:
            self.sanity = 0
            pass

    def on_collision(self, other_go):
        #testa se pode pegar objeto colidindo
        if other_go.has_tag("instrument_left"):
            self.can_get_item = other_go
            return
        else:
            self.can_get_item = None

        # precisa rechecar a colisão se houve alguma modificação
        if other_go.rigid and other_go.rect.colliderect(self.rect):
            move_rel = Point(self.dest.topleft) - Point(self.last_pos)
            while other_go.rect.colliderect(self.rect) and move_rel != Point(0, 0):
                if move_rel.x:
                    self.dest.x -= move_rel.x / abs(move_rel.x)
                    move_rel.x += - move_rel.x / abs(move_rel.x)
                if move_rel.y:
                    self.dest.y -= move_rel.y / abs(move_rel.y)
                    move_rel.y += - move_rel.y / abs(move_rel.y)


class Instrument (GameObject):

    def __init__(self, game_data):

        self.animation_names = ["guitar", "electric_guitar", "keyboard"]

        GameObject.__init__(self, "interface_instruments", game_data)
        self.fixed = True
        self.tags.append("instrument")
        self._layer = 12
        self.current_animation_name = "electric_guitar"
        self.dest = Rect(1600, 630, 0, 0)
        self.scale = 3

    def render(self):

        self.system.blit("Interface", Rect(1500, 600, 128, 128), fixed=True, scale=4)

        GameObject.render(self)