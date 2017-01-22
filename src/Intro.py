import pygame

from Salas import Deserto, Floresta, Masmorra, Gelo
from Level1 import Level1
from engine import Scene


class Intro(Scene):

    def start(self, game_data):
        self.imgs = "blind_"
        self.index = 1
        self.start_time = pygame.time.get_ticks()
        Scene.start(self, game_data)
        self.state = self.STATE_FINISHED

    def update(self):
        self.index = (pygame.time.get_ticks() - self.start_time) // 5000 + 1
        if self.index == 6:
            self.index = 5
            self.state = self.STATE_FINISHED
        Scene.update(self)

    def render(self):
        self.system.blit(self.imgs + str(self.index), pygame.Rect((0, 0), self.screen_size))

    def finish(self):
        self.system.swap_scene(Floresta())
        self.shared['scenes'] = [Floresta, Deserto, Masmorra, Gelo]
