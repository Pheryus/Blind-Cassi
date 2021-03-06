import pygame

from Salas import Deserto, Floresta, Masmorra, Gelo
from Level1 import Level1
from engine import Scene


class Intro(Scene):

    def start(self, game_data):
        self.movie = False
        self.imgs = "blind_"
        self.index = 1
        self.start_time = pygame.time.get_ticks()
        Scene.start(self, game_data)

    def resume(self):
        self.movie = False
        self.index = 1
        self.start_time = pygame.time.get_ticks()
        for obj in ('player', 'brain', 'musicicon', 'music', 'instrument'):
            try:
                self.shared.pop(obj)
            except:
                pass

    def update(self):
        for e in self.system.get_events():
            if e.type is pygame.KEYDOWN and e.key == pygame.K_SPACE:
                if self.movie:
                    self.state = self.STATE_PAUSED
                else:
                    self.movie = True

        if self.movie:
            self.index = (pygame.time.get_ticks() - self.start_time) // 5000 + 1
            if self.index == 6:
                self.index = 5
                self.state = self.STATE_PAUSED
            Scene.update(self)

    def render(self):
        if self.movie:
            self.system.blit(self.imgs + str(self.index), pygame.Rect((0, 0), self.screen_size))
        else:
            self.system.blit('tela_inicial', pygame.Rect((0,0),self.screen_size))

    def pause(self):
        self.system.push_scene(Floresta())
        self.shared['scenes'] = [Floresta, Deserto, Masmorra, Gelo]
