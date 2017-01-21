
import pygame
from random import random, choice
from engine import Scene, GameObject, Point, Physics
from DebugInfo import DebugInfo
from Player import Player
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

        self.tilemap = TileMap("mapa", game_data)
        Scene.start(self, game_data)
        self.system.camera_target = self.game_objects[1]
        self.system.camera_limits = pygame.Rect((0,0), self.tilemap.get_size())



class Vision(GameObject):

    STATE_DARKNESS = 1
    STATE_LIGHTUP = 2
    STATE_LIGHTDOWN = 3

    def __init__(self, game_data):
        GameObject.__init__(self, None, game_data)
        self.vel_expansion = 1.4
        self.surface = pygame.Surface((1920, 1080))
        self.surface.set_alpha(200)   #DEBUG
        self.surface.set_colorkey((0, 255, 0))
        self.dest = pygame.Rect(0, 0, 0, 0)
        self.position = Point(0, 0)
        self.r1 = 0
        self.r2 = 0
        self._layer = 9
        self.r_limit = 1000
        self.state = self.STATE_DARKNESS

    def render(self):
        pygame.gfxdraw.box(self.surface, pygame.Rect(0,0, 1920, 1080), (0, 0, 0))

        #r1
        pygame.gfxdraw.filled_circle(self.surface, self.position.x, self.position.y, int(self.r1), (0, 255, 0))

        #r2
        pygame.gfxdraw.filled_circle(self.surface, self.position.x, self.position.y, int(self.r2), (0, 0, 0))

        self.system.screen.blit(self.surface, (0, 0))
        # pass

    def darkness(self):
        for event in self.system.get_events():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #self.position = Point(960, 540)
                    self.position = Point(self.scene.get_gos_with_tag("player")[0].dest.center) - self.system.camera.topleft
                    self.state = self.STATE_LIGHTUP
                    self.dest.topleft = self.position - Point(self.r_limit, self.r_limit)
                    self.dest.size = Point(self.r_limit, self.r_limit) * 2
                    ##################
                    Sound.play('rock.wav')


    def lightdown(self):
        self.r2 += self.vel_expansion * self.system.delta_time
        if self.r2 >= self.r_limit:
            self.r1 = self.r2 = 0
            self.state = self.STATE_DARKNESS
            self.dest = pygame.Rect(0, 0, 0, 0)



    def lightup(self):
        self.r1 += self.vel_expansion * self.system.delta_time

        for event in self.system.get_events():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.state = self.STATE_LIGHTDOWN
                    Sound.fadeout(1000)


        if self.r1 >= self.r_limit:
            self.r1 = self.r_limit
            self.state = self.STATE_LIGHTDOWN
            Sound.fadeout(1000)


    def update(self):

        if self.state is self.STATE_DARKNESS:

            self.darkness()

        elif self.state is self.STATE_LIGHTUP:
            self.lightup()

        elif self.state is self.STATE_LIGHTDOWN:
            self.lightdown()

