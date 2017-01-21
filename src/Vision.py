import pygame

from engine import GameObject
from engine import Point


class Vision(GameObject):

    STATE_DARKNESS = 1
    STATE_LIGHTUP = 2
    STATE_LIGHTDOWN = 3

    def __init__(self, game_data):
        GameObject.__init__(self, None, game_data)

        self.vel_expansion = 1.4
        self.tags.append("music")
        self.surface = pygame.Surface((1920, 1080))
        self.surface.set_alpha(240)   #DEBUG
        self.surface.set_colorkey((0, 255, 0))
        self.dest = pygame.Rect(0, 0, 0, 0)

        self.player_ref = None



        self.position = Point(0, 0)
        self.r1 = 0
        self.r2 = 0
        self._layer = 9
        self.r_limit = 1000
        self.state = self.STATE_DARKNESS

    def render(self):
        pygame.gfxdraw.box(self.surface, pygame.Rect(0,0, 1920, 1080), (0, 0, 0))
        new_position = Point(self.player_ref.rect.center) - self.system.camera.topleft

        #r1
        pygame.gfxdraw.filled_circle(self.surface, new_position.x, new_position.y, int(self.r1), (0, 255, 0))

        #r2
        pygame.gfxdraw.filled_circle(self.surface, new_position.x, new_position.y, int(self.r2), (0, 0, 0))

        self.system.screen.blit(self.surface, (0, 0))
        pass

    def darkness(self):
        for event in self.system.get_events():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #self.position = Point(960, 540)
                    self.position = Point(self.player_ref.rect.center) #- self.system.camera.topleft
                    self.state = self.STATE_LIGHTUP
                    self.dest.center = self.position
                    #self.dest.size = Point(self.r_limit, self.r_limit) * 2
                    ##################
                    self.system.sounds.play('guitarra')


    def lightdown(self):
        self.r2 += self.vel_expansion * self.system.delta_time
        if self.r2 >= self.r_limit:
            self.r1 = self.r2 = 0
            self.state = self.STATE_DARKNESS
            self.dest = pygame.Rect(0, 0, 0, 0)

    def lightup(self):

        expansion = self.vel_expansion * self.system.delta_time

        self.r1 += expansion
        center = self.dest.center
        self.dest.size += Point(expansion*2, expansion*2)
        self.dest.center = center

        for event in self.system.get_events():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.state = self.STATE_LIGHTDOWN
                    self.system.sounds.fadeout('guitarra', 1000)

        if self.r1 >= self.r_limit:
            self.r1 = self.r_limit
            self.state = self.STATE_LIGHTDOWN
            self.system.sounds.fadeout('guitarra', 1000)

    def update(self):

        if not self.player_ref:
            self.player_ref = self.scene.get_gos_with_tag("player")[0]


        if self.state is self.STATE_DARKNESS:

            self.darkness()

        elif self.state is self.STATE_LIGHTUP:
            self.lightup()

        elif self.state is self.STATE_LIGHTDOWN:
            self.lightdown()

        for event in self.system.get_events():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.system.set_fullscreen(True)


    #def render(self):
     #   self.system.draw_geom("box", rect = self.rect, color = (0,255,0,150), fixed = True)
