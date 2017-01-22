
import pygame
from random import random, choice

from pygame.rect import Rect

from Brain import Brain
from Gotas import Gotas
from Instrument_floor import Instrument_floor
from MusicIcon import MusicIcon
from engine import Scene, GameObject, Point, Physics
from DebugInfo import DebugInfo
from Player import Player, Instrument
from Enemy import Enemy
from Vision import Vision
from Door import Door
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
        self.game_objects.append(MusicIcon(game_data))
        self.game_objects.append(Gotas(game_data))
        self.game_objects.append(Enemy(game_data, (500, 500)))
        self.game_objects.append(Instrument(game_data))

        self.game_objects.append(Instrument_floor(game_data, "keyboard", (83 * 47, 52 * 47)))

        self.tilemap = TileMap("mapa", game_data)
        Scene.start(self, game_data)
        #self.system.sounds.play("background_music")
        self.system.camera_target = self.game_objects[1]
        self.system.camera_limits = pygame.Rect((0,0), self.tilemap.get_size())