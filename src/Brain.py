import pygame
from pygame.rect import Rect

from engine import GameObject
from engine import Point


class Brain(GameObject):

    def __init__(self, game_data):
        GameObject.__init__(self, "cerebro", game_data)

        self.tags.append("brain")
        self._layer = 12
        self.dest = Rect(10, 20, 0, 0)
        self.scale = 0.5
        self.fixed = True
        self.player_ref = None
        self.font_surface = pygame.Surface((100, 100))

    def update(self):
        if not self.player_ref:
            self.player_ref = self.scene.get_gos_with_tag("player")[0]

    def render(self):
        if self.player_ref:
            self.system.draw_font(str(self.player_ref.sanity)[:3], "8bit16.ttf", 30, Point(self.rect.midtop),
                                  color = (255, 255, 255), centered=False, fixed=True)
        GameObject.render(self)