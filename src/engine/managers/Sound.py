from pygame.mixer import music
from pygame.mixer import Sound as pygame_sound
import os
from os.path import isdir
from os import listdir
import sys

GAME_DIR = os.path.dirname(os.path.abspath(sys.argv[0])) + "/../"
MUSIC_PATH = GAME_DIR + "/etc/sound/"
SHARED_FOLDER = "shared/"
FORMATS_SUPPORTED = ['mp3', 'wav', 'ogg']


class Sound:
    def __init__(self):
        self.path = MUSIC_PATH
        self.songs = dict()
        self.load(SHARED_FOLDER)

    def load(self, folder):
        if folder[-1] != '/':
            folder += "/"
        # se pasta existe e é realmente uma pasta
        if isdir(self.path + folder):
            files = listdir(self.path + folder)
            # pra cada arquivo na pasta
            for file in files:
                name = file[:-4]
                extension = file[-3:]
                # testa se a extensão é uma dessas 3
                if extension in FORMATS_SUPPORTED:
                    # carrega a imagem e põe no dicionario
                    self.songs[name] = pygame_sound(self.path + folder + file)

    def unload(self, folder):
        if folder[-1] != '/':
            folder += "/"
        # se pasta existe e é realmente uma pasta
        if isdir(self.path + folder):
            files = listdir(self.path + folder)
            # pra cada arquivo na pasta
            for file in files:
                name = file[:-4]
                extension = file[-3:]
                # testa se a extensão é uma dessas 3
                if extension in FORMATS_SUPPORTED:
                    # carrega a imagem e põe no dicionario
                    self.songs.pop(name)

    def play(self, song):
        self.songs[song].play()

    def stop(self, song):
        self.songs[song].stop()

    def fadeout(self, song, time):
        self.songs[song].fadeout(time)

    def set_volume(self, song, value):
        self.songs[song].set_volume(value)

def play(song, loops=-1, start=0.0):
    volume = get_volume()
    if music.get_busy():
        fadeout(1000)
    music.load(MUSIC_PATH + song)
    music.play(loops, start)
    set_volume(volume)


def instant_play(song, loops=-1, start=0.0):
    volume = get_volume()
    music.stop()
    music.load(MUSIC_PATH + song)
    music.play(loops, start)
    set_volume(volume)


def fadeout(time):
    music.fadeout(time)


def queue(song):
    music.queue(MUSIC_PATH + song)


def replay(loops=-1, start=0.0):
    music.play(loops, start)


def pause():
    music.pause()


def resume():
    music.unpause()


def get_volume():
    return music.get_volume()

def set_volume(value):
    return music.set_volume(value)


def stop():
    music.stop()


def is_playing(song=None):
    if song:
        pass
    return music.get_busy()
