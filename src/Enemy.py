import pygame
from random import random, choice
from engine import Scene, GameObject, Point, Physics
import math



class Enemy(GameObject):

    STATE_LEFT = 1
    STATE_RIGHT = 2
    STATE_UP = 3
    STATE_DOWN = 4

    AGGRO_VISION = 300
    AGGRO_AUDITION = 600

    SPEAKING = 1000


    SANITY_DRAIN_MIN = 5
    SANITY_DRAIN_MAX = 40

    SANITY_RANGE = 400

    def __init__(self, game_data, pos, state = 4):
        self.animation_names = ['up', 'down', 'left', 'right']
        GameObject.__init__(self, 'monster', game_data)


        self.tags.append("enemy1")
        self._layer = 2
        self.current_animation_name = 'down'

        self.dest = pygame.Rect(pos[0], pos[1], 0, 0)
        self.scale = 3

        center_point = self.rect.center

        self.player_ref = None
        self.sound_ref = None
        self.is_hearing = False
        self.is_seeing = False
        self.is_damaging = False

        self.vision_rect = pygame.Rect(0, 0, self.AGGRO_VISION, self.AGGRO_VISION)
        self.vision_rect.center = self.rect.center
        self.audition_rect = pygame.Rect(0, 0, self.AGGRO_AUDITION, self.AGGRO_AUDITION)
        self.audition_rect.center = self.rect.center


    def listen(self):
        return self.audition_rect.colliderect(self.sound_ref.rect)

    def vision_field(self):
        return self.vision_rect.colliderect(self.player_ref.rect)

    def move(self):
        self.vision_rect.center = self.rect.center

    def get_player_ref(self):
        self.player_ref = self.scene.get_gos_with_tag("player")[0]

    def get_sound_ref(self):
        self.sound_ref = self.scene.get_gos_with_tag("music")[0]

    def update(self):

        if not self.sound_ref:
            self.get_sound_ref()

        if not self.player_ref:
            self.get_player_ref()

        elif self.vision_field() or self.listen():
            self.sanity_drop()

        GameObject.update(self)

    def get_distance_to_player(self):
        return math.hypot(self.player_ref.rect.x - self.rect.x, self.player_ref.rect.y - self.rect.y)

    def sanity_drop(self):

        distance = self.get_distance_to_player()

        if distance == 0:
            distance = 0.1

        sanity = (self.AGGRO_AUDITION / distance ) * (self.system.delta_time / 1000) * self.SANITY_DRAIN_MIN

        if sanity > self.SANITY_DRAIN_MAX:
            sanity = self.SANITY_DRAIN_MAX

        self.player_ref.sanity -= sanity

        #self.scene.tilemap.get_shortest_path(Point(self.rect.center), Point(music_pos.rect.center))

    def render(self):

        #self.system.draw_geom("box", rect = self.sound_ref.rect, color = (0, 0, 255, 110))
        #self.system.draw_geom("box", rect=self.vision_rect, color=(155, 0, 155, 150))
        #self.system.draw_geom("box", rect = self.audition_rect, color = (0,0,0,150) )
        GameObject.render(self)