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

    SANITY_DRAIN_MIN = 1
    SANITY_DRAIN_MAX = 5

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

        self.vision_rect = pygame.Rect(0, 0, self.AGGRO_VISION, self.AGGRO_VISION)
        self.vision_rect.center = self.rect.center
        self.audition_rect = pygame.Rect(0, 0, self.AGGRO_AUDITION, self.AGGRO_AUDITION)
        self.audition_rect.center = self.rect.center


    def listen(self, sound_pos):

        print(self.audition_rect, sound_pos)
        return self.audition_rect.colliderect(sound_pos)

    def vision_field(self):
        return self.vision_rect.colliderect(self.player_ref.rect)

    def move(self):
        self.vision_rect.center = self.rect.center

    def get_player_ref(self):
        self.player_ref = self.scene.get_gos_with_tag("player")[0]

    def update(self):

        if not self.player_ref:
            self.get_player_ref()

        # viu
        if self.vision_field():
            print("achou")
        GameObject.update(self)



        #self.scene.tilemap.get_shortest_path(Point(self.rect.center), Point(music_pos.rect.center))
    def render(self):
        self.system.draw_geom("box", rect = self.audition_rect, color=(0,0,0,150))

        self.system.draw_geom("box", rect=self.player_ref.rect, color=(0, 0, 255, 150))
        GameObject.render(self)