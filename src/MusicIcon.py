import pygame

from engine import GameObject


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
        self.tags.append("musicicon")

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
