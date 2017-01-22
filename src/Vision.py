import pygame

from engine import GameObject
from engine import Point


class Vision(GameObject):

    STATE_DARKNESS = 1
    STATE_LIGHTUP = 2
    STATE_LIGHTDOWN = 3
    STATE_COOLDOWN = 4

    def __init__(self, game_data):
        GameObject.__init__(self, None, game_data)


        self.game_data = game_data

        self.vel_expansion = 400
        self.tags.append("music")
        self.surface = pygame.Surface((1920, 1080)).convert_alpha()
        # self.surface.set_alpha(240)   #DEBUG
        # self.surface.set_colorkey((0, 255, 0))
        self.dest = pygame.Rect(0, 0, 0, 0)
        self.player_ref = None
        self.position = Point(0, 0)
        self.r1 = 0
        self.r2 = 0
        self._layer = 9
        self.r_limit = 400
        self.state = self.STATE_DARKNESS
        self.cooldown_time = 0

    def render(self):
        pygame.draw.rect(self.surface, (0, 0, 0, 255), pygame.Rect(0,0, 1920, 1080))
        new_position = Point(self.player_ref.rect.center) - self.system.camera.topleft

        #r1
        pygame.draw.circle(self.surface, (0, 0, 0, 0), new_position, int(self.r1))

        #r2
        pygame.draw.circle(self.surface, (0, 0, 0, 230), new_position, int(self.r2))

        self.system.screen.blit(self.surface, (0, 0))
        pass

    def darkness(self):
        for event in self.system.get_events():
            if event.type == pygame.KEYDOWN:
                if event.key == self.player_ref.CONTROL["play_song"]:

                    destino = Point(self.player_ref.dest.x - self.player_ref.rect.w, self.player_ref.dest.y - self.player_ref.rect.h)

                    self.scene.game_objects.append(SoundAnimation(self.game_data, destino))
                    self.scene.layers.add(self.scene.game_objects[-1])

                    #self.position = Point(960, 540)

                    self.player_ref.state = self.player_ref.STATE_PLAYING

                    self.player_ref.current_animation_name = self.player_ref.instruments[self.player_ref.instrument_index][0]
                    self.position = Point(self.player_ref.rect.center) #- self.system.camera.topleft
                    self.state = self.STATE_LIGHTUP
                    self.dest.center = self.position
                    #self.dest.size = Point(self.r_limit, self.r_limit) * 2
                    ##################
                    self.system.sounds.play(self.player_ref.instruments[self.player_ref.instrument_index][0])


    def lightdown(self):
        self.r2 += self.vel_expansion * self.system.delta_time / 1000
        if self.r2 >= self.r1:
            self.player_ref.current_animation_name = "stand_down"
            self.r1 = self.r2 = 0
            self.state = self.STATE_COOLDOWN
            self.dest = pygame.Rect(0, 0, 0, 0)

    def lightup(self):

        expansion = self.vel_expansion * self.system.delta_time / 1000
        self.cooldown_time += self.system.delta_time

        self.r1 += expansion
        center = self.dest.center
        self.dest.size += Point(expansion*2, expansion*2)
        self.dest.center = center

        for event in self.system.get_events():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.state = self.STATE_LIGHTDOWN

                    self.system.sounds.fadeout(self.player_ref.instruments[self.player_ref.instrument_index][0], self.cooldown_time)

        if self.r1 >= self.r_limit:
            self.r1 = self.r_limit

        if self.cooldown_time >= 3000:
            self.state = self.STATE_LIGHTDOWN
            self.system.sounds.fadeout(self.player_ref.instruments[self.player_ref.instrument_index][0], self.cooldown_time)

    def cooldown(self):
        self.cooldown_time -= self.system.delta_time
        if self.cooldown_time <= 0:
            self.state = self.STATE_DARKNESS
            self.cooldown_time = 0

    def update(self):

        if not self.player_ref:
            self.player_ref = self.scene.get_gos_with_tag("player")[0]

        if self.state is self.STATE_DARKNESS:
            self.darkness()

        elif self.state is self.STATE_LIGHTUP:
            self.lightup()

        elif self.state is self.STATE_LIGHTDOWN:
            self.lightdown()

        elif self.state is self.STATE_COOLDOWN:
            self.cooldown()

        for event in self.system.get_events():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.system.set_fullscreen(True)

    #def render(self):
     #   self.system.draw_geom("box", rect = self.rect, color = (0,255,0,150), fixed = True)
