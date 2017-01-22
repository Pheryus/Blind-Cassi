import pygame
from pygame.rect import Rect

from engine import GameObject


class SoundAnimation(GameObject):
    def __init__(self, game_data, pos):
        self.animation_names = ['sound']

        GameObject.__init__(self, 'sound_animation', game_data)

        self.animation.num_loops = 1
        self._layer = 5
        self.dest = Rect(pos[0], pos[1], 0, 0)
        self.scale = 1
        self.loops = 0


    def update(self):

        if self.animation.is_finished():
            self.kill()

        GameObject.update(self)