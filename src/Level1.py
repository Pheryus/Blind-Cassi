import pygame

from Brain import Brain
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

    def start(self, game_data):

        # self.game_objects.append(Vision(game_data))
        # self.game_objects.append(Player(game_data, (30 * 96, 30 * 96)))
        # self.game_objects.append(Instrument(game_data))
        # self.game_objects.append(DebugInfo(game_data))
        # self.game_objects.append(Brain(game_data))
        # self.game_objects.append(MusicIcon(game_data))
        #
        # self.game_objects.append(Instrument_floor(game_data, "keyboard", (30 * 96, 30 * 96)))
        #
        # self.game_objects.append(Enemy("electric_guitar", (1770, 2200), game_data))
        # self.game_objects.append(Enemy("guitar", (876, 2871), game_data))
        # self.game_objects.append(Enemy("electric_guitar", (2016, 373), game_data))
        # self.game_objects.append(Enemy("monster", (2162, 442), game_data))

        if not Sound.is_playing("background_music.ogg"):
            Sound.play("background_music.ogg")
        for tipo, pos_list in self.enemies_dict.items():
            for pos in pos_list:
                self.game_objects.append(Enemy(tipo, pos * 96, game_data))

        self.dead = False
        shared = game_data['shared']

        if shared.get('player'):
            self.game_objects.append(shared['player'])
        else:
            self.game_objects.append(Player(game_data, (0, 0)))

        self.game_objects[-1].dest.topleft = self.player_pos * 96

        if self.instrument:
            for instrument in self.game_objects[-1].instruments:
                print(instrument)
                if self.instrument in instrument:
                    if instrument[1]:
                        break
            else:
                self.game_objects.append(
                    Instrument_floor(game_data, self.instrument, self.instrument_pos * 96))
                # self.game_objects[-1].dest.topleft = self.instrument_pos

        if shared.get('music'):
            self.game_objects.append(shared['music'])
        else:
            self.game_objects.append(Vision(game_data))

        if shared.get('brain'):
            self.game_objects.append(shared['brain'])
        else:
            self.game_objects.append(Brain(game_data))

        if shared.get('musicicon'):
            self.game_objects.append(shared['musicicon'])
        else:
            self.game_objects.append(MusicIcon(game_data))

        if shared.get('instrument'):
            self.game_objects.append(shared['instrument'])
        else:
            self.game_objects.append(Instrument(game_data))


        self.tilemap = TileMap(self.name, game_data)
        Scene.start(self, game_data)
        self.system.camera_target = self.get_gos_with_tag('player')[0]
        self.system.camera_limits = pygame.Rect((0, 0), self.tilemap.get_size())

    def update(self):
        Scene.update(self)
        player = self.get_gos_with_tag('player')[0]
        if self.previous == 'up':
            if player.rect.bottom <= self.system.camera_limits.top:
                self.state = self.STATE_FINISHED
                self.next = None
        elif self.previous == 'down':
            if player.rect.top >= self.system.camera_limits.bottom:
                self.state = self.STATE_FINISHED
                self.next = None
        elif self.previous == 'left':
            if player.rect.right <= self.system.camera_limits.left:
                self.state = self.STATE_FINISHED
                self.next = None
        elif self.previous == 'right':
            if player.rect.left >= self.system.camera_limits.right:
                self.state = self.STATE_FINISHED
                self.next = None

        if self.next == 'up':
            if player.rect.bottom <= self.system.camera_limits.top:
                self.state = self.STATE_FINISHED
                self.previous = None
        elif self.next == 'down':
            if player.rect.top >= self.system.camera_limits.bottom:
                self.state = self.STATE_FINISHED
                self.previous = None
        elif self.next == 'left':
            if player.rect.right <= self.system.camera_limits.left:
                self.state = self.STATE_FINISHED
                self.previous = None
        elif self.next == 'right':
            if player.rect.left >= self.system.camera_limits.right:
                self.state = self.STATE_FINISHED
                self.previous = None

    def finish(self):
        index = None
        if self.dead:
            index = 0
        elif not self.previous:
            index = self.shared['scenes'].index(type(self)) + 1
        elif not self.next:
            index = self.shared['scenes'].index(type(self)) - 1

        if index is not None:
            self.system.swap_scene(self.shared['scenes'][index]())

            for name in ('player', 'music', 'brain', 'musicicon', 'instrument'):
                if not self.shared.get(name):
                    self.shared[name] = self.get_gos_with_tag(name)[0]
