import pygame
from random import random, choice

from pygame.rect import Rect

from engine import Scene, GameObject, Point, Physics

class Door(GameObject):
    def __init__(self, game_data, instrument_to_open, pos, horizontal = True):

        if horizontal:
            GameObject.__init__(self, "door_horizontal", game_data)
        else:
            GameObject.__init__(self, "door_vertical", game_data)

        self.layer = 3
        self.dest = Rect(pos[0], pos[1], 0, 0)
        self.scale = 1
        self.sound_ref = None

    def update(self):
        if not self.sound_ref:
            self.sound_ref = self.scene.get_gos_with_tag("music")[0]

        elif self.rect.colliderect(self.sound_ref.rect):
            self.system.sounds.play("door")
            self.kill()