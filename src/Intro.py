import pygame

from Brain import Brain
from Instrument_floor import Instrument_floor
from MusicIcon import MusicIcon
from engine import Scene, GameObject, Point, Physics
from DebugInfo import DebugInfo
from Player import Player, Instrument
from Enemy import Enemy
from Vision import Vision

from engine.TileMap import TileMap

class Intro(Scene):

    def __init__(self):
        Scene.__init__(self, "Intro")


