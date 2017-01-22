import pygame
from pygame import Rect, time

from engine import GameObject


class Gotas(GameObject):
    def __init__(self, game_data, pos=(0,0), scale=2):
        self.animation_names = ['gota']

        GameObject.__init__(self, "gotas", game_data)

        self.time = 0
        self.seconds = 0
        self.new_surface = pygame.Surface((800, 800))
        self._layer = 4
        self.dest = Rect(83 * 46, 52 * 48, 0, 0)
        self.scale = scale
        self.raio = 500 * scale

    def render(self):
        #pygame.gfxdraw.filled_circle(self.new_surface, self.dest.center[0], self.dest.center[1], int(self.raio), (255, 255, 255))
        #self.system.screen.blit(self.new_surface, (0, 0))
        GameObject.render(self)

    def update(self):
        self.time += self.system.delta_time
        if self.time >= 4000:
            self.system.sounds.play("drop")
            self.time = 0
