
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
        self.game_objects.append(DebugInfo(game_data))
        self.game_objects.append(Player(game_data))

        self.game_objects.append(Vision(game_data))
        self.game_objects.append(Brain(game_data))
        self.game_objects.append(MusicIcon(game_data))
        self.game_objects.append(Enemy("monster", (16 * 48, 25 * 48), game_data))
        self.game_objects.append(Instrument(game_data))

        self.tilemap = TileMap("mapa", game_data)
        Scene.start(self, game_data)
        self.system.camera_target = self.game_objects[1]
        self.system.camera_limits = pygame.Rect((0,0), self.tilemap.get_size())
        self.system.camera_limits = pygame.Rect(0,0, 10000, 10000)

class MusicIcon(GameObject):
    STATE_NO_MUSIC = 1,
    STATE_PLAYING = 2,
    STATE_COOLDOWN = 3

    def __init__(self, game_data):
        self.animation_names = ['no_music', 'playing', 'cooldown']
        GameObject.__init__(self, 'music', game_data)
        self.state = self.STATE_NO_MUSIC
        self.dest = pygame.Rect(1920 - 122, 10, 112, 112)
        self.fixed = True
        self._layer = 10

    def update(self):
        vision = self.scene.get_gos_with_tag('music')[0]

        if self.state is self.STATE_NO_MUSIC:
            if vision.state is vision.STATE_LIGHTUP:
                self.state = self.STATE_PLAYING
                self.current_animation_name = "playing"

        elif self.state is self.STATE_PLAYING:
            if vision.state is vision.STATE_COOLDOWN:
                self.state = self.STATE_COOLDOWN
                self.current_animation_name = "cooldown"

        elif self.state is self.STATE_COOLDOWN:
            if vision.state is vision.STATE_DARKNESS:
                self.state = self.STATE_NO_MUSIC
                self.current_animation_name = "no_music"

        GameObject.update(self)

    def render(self):
        vision = self.scene.get_gos_with_tag('music')[0]
        # TODO fazer sonzinhos
        GameObject.render(self)

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
            self.system.draw_font(str(self.player_ref.sanity)[:2], "8bit16.ttf", 30, Point(self.rect.midtop),
                                  color = (255, 255, 255), centered=False, fixed=True)
        GameObject.render(self)

