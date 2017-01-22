import pygame

from Brain import Brain
from Door import Door
from Instrument_floor import Instrument_floor
from MusicIcon import MusicIcon
from engine import Scene, GameObject, Point, Physics
from DebugInfo import DebugInfo
from engine.managers import Sound
from Player import Player, Instrument
from Enemy import Enemy
from Vision import Vision

from engine.TileMap import TileMap

class Level1(Scene):

    def __init__(self):
        Scene.__init__(self, "Floresta")

    def start(self, game_data):
        Sound.play("background_music.ogg")
        self.game_objects.append(Vision(game_data))
        self.game_objects.append(Player(game_data, (30 * 96, 30 * 96)))
        self.game_objects.append(Instrument(game_data))
        #self.game_objects.append(DebugInfo(game_data))
        self.game_objects.append(Brain(game_data))
        self.game_objects.append(MusicIcon(game_data))

        self.game_objects.append(Instrument_floor(game_data, "keyboard", (30 * 96, 30 * 96)))

        self.game_objects.append(Enemy("electric_guitar", (1770, 2200), game_data))
        self.game_objects.append(Enemy("guitar", (876, 2871), game_data))
        self.game_objects.append(Enemy("electric_guitar", (2016, 373), game_data))
        self.game_objects.append(Enemy("monster", (2162, 442), game_data))

        self.game_objects.append(Door(game_data, "keyboard", (95, 1266), False))

        #self.game_objects.append(Instrument(game_data))

        #self.game_objects.append(Instrument_floor(game_data, "keyboard", (83 * 47, 52 * 47)))

        self.tilemap = TileMap("Floresta", game_data)
        Scene.start(self, game_data)
        self.system.camera_target = self.game_objects[1]
        self.system.camera_limits = pygame.Rect((0, 0), self.tilemap.get_size())
