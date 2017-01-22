import pygame
from random import random, choice
from engine import Scene, GameObject, Point, Physics
import math



class Enemy(GameObject):

    STATE_STANDBY = 7
    STATE_PURSUE = 6

    AGGRO_VISION = 300
    AGGRO_AUDITION = 600


    SANITY_DRAIN_MIN = 5
    SANITY_DRAIN_MAX = 40

    SANITY_RANGE = 400

    def __init__(self, type_, pos, game_data):
        self.animation_names = list()
        for side in ('up', 'down', 'left', 'right'):
            self.animation_names += ["walking_" + side, "stand_" + side]
        GameObject.__init__(self, "monster_" + type_, game_data)

        self.tags.append(type_)
        self._layer = 5
        self.current_animation_name = 'stand_down'

        self.dest = pygame.Rect(pos[0], pos[1], 0, 0)
        self.scale = 3

        self.last_pos = self.dest.topleft
        self.player_ref = None
        self.sound_ref = None
        self.is_hearing = False
        self.is_seeing = False
        self.is_damaging = False

        self.vision_rect = pygame.Rect(0, 0, self.AGGRO_VISION, self.AGGRO_VISION)
        self.vision_rect.center = self.rect.center
        self.audition_rect = pygame.Rect(0, 0, self.AGGRO_AUDITION, self.AGGRO_AUDITION)
        self.audition_rect.center = self.rect.center
        self.state = self.STATE_STANDBY
        self.waypoints = []
        self.vel = 250
        self.normal = lambda x: x / abs(x)

    def listen(self):
        if not self.sound_ref:
            self.get_sound_ref()
        return self.audition_rect.colliderect(self.sound_ref.rect)

    def vision_field(self):
        if not self.player_ref:
            self.get_player_ref()
        return self.vision_rect.colliderect(self.player_ref.rect)

    def move(self):
        self.vision_rect.center = self.rect.center

    def get_player_ref(self):
        self.player_ref = self.scene.get_gos_with_tag("player")[0]

    def get_sound_ref(self):
        self.sound_ref = self.scene.get_gos_with_tag("music")[0]

    def update(self):
        self.last_pos = self.dest.topleft

        if self.vision_field() or self.listen():
            self.sanity_drop()
            self.target = Point(self.player_ref.rect.center)
            self.state = self.STATE_PURSUE

        if self.state == self.STATE_PURSUE:
            distance = self.target - self.dest.center
            vel_frame = self.vel * self.system.delta_time / 1000
            if distance.x != 0:
                if abs(distance.x) <= vel_frame:
                    self.dest.x = self.target.x - self.rect.w // 2
                else:
                    self.dest.x += self.normal(distance.x) * vel_frame
                    self.current_animation_name = "walking_left" if self.normal(
                        distance.x) == -1 else "walking_right"
            if distance.y != 0:
                if abs(distance.y) <= vel_frame:
                    self.dest.y = self.target.y - self.rect.h // 2
                else:
                    self.dest.y += self.normal(distance.y) * vel_frame
                    self.current_animation_name = "walking_up" if self.normal(
                        distance.y) == -1 else "walking_down"
            if distance.x == 0 and distance.y == 0:
                self.state = self.STATE_STANDBY

        elif self.state == self.STATE_STANDBY:
            for side in ("up", "down", "left", "right"):
                if self.current_animation_name == "walking_" + side:
                    self.current_animation_name = "stand_" + side
                    break

    def get_distance_to_player(self):
        return math.hypot(self.player_ref.rect.x - self.rect.x, self.player_ref.rect.y - self.rect.y)

    def sanity_drop(self):

        distance = self.get_distance_to_player()
        if distance == 0:
            distance = 0.1
        sanity = (self.AGGRO_AUDITION / distance) * (self.system.delta_time / 1000) * self.SANITY_DRAIN_MIN

        if sanity > self.SANITY_DRAIN_MAX:
            sanity = self.SANITY_DRAIN_MAX

        self.player_ref.sanity -= sanity

    def on_collision(self, other_go):
        # precisa rechecar a colisão se houve alguma modificação
        if other_go.rigid and other_go.rect.colliderect(self.rect):
            move_rel = Point(self.dest.topleft) - Point(self.last_pos)
            while other_go.rect.colliderect(self.rect) and move_rel != Point(0,
                                                                             0):
                if move_rel.x:
                    self.dest.x -= self.normal(move_rel.x)
                    move_rel.x -= self.normal(move_rel.x)
                if move_rel.y:
                    self.dest.y -= self.normal(move_rel.y)
                    move_rel.y -= self.normal(move_rel.y)

            self.state = self.STATE_STANDBY