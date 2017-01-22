from Level1 import Level1
from engine import Point


class Deserto(Level1):

    def __init__(self):
        Level1.__init__(self, "Deserto")

    def start(self, game_data):
        self.previous = ""
        self.next = "down"
        self.player_pos = Point(21, 16)
        self.enemies_dict = {
            "guitar": [],
            "eletric_guitar": [],
            "keyboard": []
        }
        self.instrument = "guitar"
        self.instrument_pos = Point(22,18)

        Level1.start(self, game_data)

class Floresta(Level1):

    def __init__(self):
        Level1.__init__(self, "Floresta")

    def start(self, game_data):
        self.previous = "up"
        self.next = "left"
        self.player_pos = Point(22, 0)
        self.enemies_dict = {
            "guitar": [],
            "eletric_guitar": [Point(22, 2)],
            "keyboard": []
        }
        self.instrument = None
        self.instrument_pos = Point(22, 1)

        Level1.start(self, game_data)

class Masmorra(Level1):

    def __init__(self):
        Level1.__init__(self, "Masmorra")

    def start(self, game_data):
        self.previous = "right"
        self.next = "up"
        self.player_pos = Point(47, 21)
        self.enemies_dict = {
            "guitar": [],
            "eletric_guitar": [],
            "keyboard": []
        }

        Level1.start(self, game_data)

class Gelo(Level1):

    def __init__(self):
        Level1.__init__(self, "Gelo")

    def start(self, game_data):
        self.previous = "down"
        self.next = "left"
        self.player_pos = Point(32, 39)
        self.enemies_dict = {
            "guitar": [],
            "eletric_guitar": [],
            "keyboard": []
        }

        Level1.start(self, game_data)