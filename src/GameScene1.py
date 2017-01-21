
import pygame
from random import random, choice

from pygame.rect import Rect

from engine import Scene, GameObject, Point, Physics
from DebugInfo import DebugInfo
from Player import Player, Instrument
from Enemy import Enemy
from Vision import Vision
from engine.managers import Sound

from engine.TileMap import TileMap


class GameScene1(Scene):

    def __init__(self):
        Scene.__init__(self, "Caverna")


    def start(self, game_data):
        #self.game_objects
        self.game_objects.append(Vision(game_data))
        self.game_objects.append(Player(game_data))
        self.game_objects.append(DebugInfo(game_data))
        self.game_objects.append(Brain(game_data))
        self.game_objects.append(Enemy(game_data, (500, 500)))
        self.game_objects.append(Instrument(game_data))
        self.tilemap = TileMap("mapa", game_data)
        Scene.start(self, game_data)
        self.system.camera_target = self.game_objects[1]
        self.system.camera_limits = pygame.Rect((0,0), self.tilemap.get_size())


class Brain(GameObject):

    def __init__(self, game_data):
        GameObject.__init__(self, "cerebro", game_data)

        self.tags.append("brain")
        self._layer = 12
        self.dest = Rect(100, 150, 0, 0)
        self.scale = 0.5
        self.fixed = True
        self.player_ref = None
        self.font_surface = pygame.Surface((100, 100))

    def update(self):

        if not self.player_ref:
            self.player_ref = self.scene.get_gos_with_tag("player")[0]

    def render(self):
        if self.player_ref:
            self.system.draw_font(str(self.player_ref.sanity)[:2], "8bit16.ttf", 30, Point(self.rect.midtop),
                                  color = (255, 255, 255), centered=False, fixed=True)
        GameObject.render(self)

