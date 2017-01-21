import json
from pygame.rect import Rect
from engine import GameObject, Point
from engine.System import GAME_DIR

TEXTURESPEC_PATH = GAME_DIR + "etc/json/"


class TileMap:
    def __init__(self, name, game_data):
        self.game_data = game_data

        self.name = name
        self.layers = list()
        self.load_json(TEXTURESPEC_PATH + self.game_data['scene'].name + "/" + name + ".json")
        self.graph = None
        for layer in self.layers:
            self.game_data['scene'].layers.add(*layer, layer=self.layers.index(layer))

    def load_json(self, jsonfile):
        with open(jsonfile) as file:
            dic = json.load(file)

        self.width = dic['width']
        self.height = dic['height']
        self.tile_width = dic['tilewidth']
        self.tile_height = dic['tileheight']
        self.properties = list()
        self.graph = [[True for i in range(self.width)] for j in range(self.height)]

        #tileset = self.game_data['system'].texturespecs.specs[self.name]['tileset']
        self.tilesets = dict()
        self.tiles = list()
        for tileset in dic['tilesets']:
            self.tilesets[tileset['name']] = {
                'range': range(tileset['firstgid'] - 1, tileset['firstgid'] + tileset['tilecount'] - 1),
                'properties': tileset.get('tileproperties')
            }
            self.tiles += self.load_tiles(tileset)

        for layer in dic['layers']:
            self.layers.append(self.load_layer(layer))

    def load_tiles(self, tileset_dic):
        class NoMoreTiles(Exception): pass

        w = tileset_dic['tilewidth']
        h = tileset_dic['tileheight']
        columns = tileset_dic['columns']
        num_tiles = tileset_dic['tilecount']
        tileset = list()
        try:
            for y in range(0, tileset_dic['imageheight'], h):
                for x in range(0, columns * w, w): # tileset_dic['imagewidth']
                    tileset.append(Rect(x, y, w, h))
                    num_tiles -= 1
                    if num_tiles is 0:
                        raise NoMoreTiles
        except NoMoreTiles:
            pass
        return tileset

    def load_layer(self, layer):
        new_layer = list()
        height = layer['height']
        width = layer['width']
        offset = Point(layer['x'], layer['y'])
        if layer['type'] == 'tilelayer':
            tile_nums = layer['data']
            for j in range(height):
                for i in range(width):
                    tile_num = tile_nums[j * width + i] - 1
                    if tile_num >= 0:
                        image_name = None
                        for _name, data in self.tilesets.items():
                            if tile_num in data['range']:
                                image_name = _name
                                break

                        go_tile = GameObject(image_name, self.game_data)
                        go_tile.src = self.tiles[tile_num]
                        go_tile.dest = Rect(
                            Point(i * self.tile_width, j * self.tile_height) + offset,
                            go_tile.src.size
                        )

                        tile_num = str(tile_num)
                        properties = self.tilesets[image_name]['properties']
                        if properties and properties.get(tile_num):
                            if properties[tile_num].get('tag'):
                                go_tile.tags.append(properties[tile_num]['tag'])
                            if properties[tile_num].get('rigid'):
                                go_tile.rigid = properties[tile_num]['rigid']
                                if go_tile.rigid:
                                    self.graph[j][i] = False
                        new_layer.append(go_tile)
        elif layer['type'] == 'imagelayer':
            image_name = layer['image'][layer['image'].rfind('/') + 1 : layer['image'].rfind('.')]
            go_image = GameObject(image_name, self.game_data)
            go_image.dest.topleft = offset
            go_image.scale = 1
            new_layer.append(go_image)
        return new_layer

    def get_size(self):
        return Point(self.width * self.tile_width, self.height * self.tile_height)

    def move_layer(self, layer, offset):
        for tile in self.layers[layer]:
            tile.dest.topleft += Point(offset)

    def get_shortest_path(self, ini, fim):
        ini = Point(ini[0] // self.tile_width, ini[1] // self.tile_height).int()
        fim = Point(fim[0] // self.tile_width, fim[1] // self.tile_height).int()
        if not self.graph[fim.y][fim.x]:
            return []

        queue = [ini]
        inside = lambda p: p.x in range(self.width) and p.y in range(self.height)
        dic = {'visited': False, 'distance': float('inf'), 'previous': None}
        spt = {ini: dic.copy()}
        spt[ini]['distance'] = 0
        vizinhos = (Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1))

        while len(queue) > 0:
            pos = queue.pop(0)
            if pos == fim:
                continue
            spt[pos]['visited'] = True
            for viz in vizinhos:
                viz = pos + viz
                if inside(viz):
                    if not spt.get(viz):
                        spt[viz] = dic.copy()
                    elif spt[viz]['visited']:
                        continue
                    if spt[pos]['distance'] + 1 < spt[viz]['distance']:
                        spt[viz]['distance'] = spt[pos]['distance'] + 1
                        spt[viz]['previous'] = pos
                        if queue.count(viz) == 0:
                            queue.append(viz)

        pos = fim
        while pos != ini:
            queue.append(pos)
            pos = spt[pos]['previous']
        queue.reverse()
        return queue