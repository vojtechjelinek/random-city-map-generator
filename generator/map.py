from pprint import pprint

class Map():

    WATER = 'W'
    GRASS = 'G'
    STREET = 'S'
    COLORS = {
        WATER: (0, 0, 255),
        GRASS: (0, 255, 0),
        STREET: (210, 210, 210)
    }
    SCALING_SIZE = 5
    SHAPES = {
        '': ((0, 0, 0, 0, 0),
             (0, 1, 1, 1, 0),
             (0, 1, 1, 1, 0),
             (0, 1, 1, 1, 0),
             (0, 0, 0, 0, 0)),
        'W': ((0, 0, 0, 0, 0),
              (1, 1, 1, 1, 1),
              (1, 1, 1, 1, 1),
              (1, 1, 1, 1, 1),
              (0, 0, 0, 0, 0)),
        'S': ((0, 1, 1, 1, 0),
              (0, 1, 1, 1, 0),
              (0, 1, 1, 1, 0),
              (0, 1, 1, 1, 0),
              (0, 1, 1, 1, 0)),
        'E': ((0, 0, 0, 0, 0),
              (1, 1, 1, 1, 1),
              (1, 1, 1, 1, 1),
              (1, 1, 1, 1, 1),
              (0, 0, 0, 0, 0)),
        'N': ((0, 1, 1, 1, 0),
              (0, 1, 1, 1, 0),
              (0, 1, 1, 1, 0),
              (0, 1, 1, 1, 0),
              (0, 1, 1, 1, 0)),
        'WS': ((0, 0, 0, 0, 0),
               (1, 0, 0, 0, 0),
               (1, 1, 0, 0, 0),
               (1, 1, 1, 0, 0),
               (1, 1, 1, 1, 0)),
        'SE': ((0, 0, 0, 0, 0),
               (0, 0, 0, 0, 1),
               (0, 0, 0, 1, 1),
               (0, 0, 1, 1, 1),
               (0, 1, 1, 1, 1)),
        'EN': ((0, 1, 1, 1, 1),
               (0, 0, 1, 1, 1),
               (0, 0, 0, 1, 1),
               (0, 0, 0, 0, 1),
               (0, 0, 0, 0, 0)),
        'WN': ((1, 1, 1, 1, 0),
               (1, 1, 1, 0, 0),
               (1, 1, 0, 0, 0),
               (1, 0, 0, 0, 0),
               (0, 0, 0, 0, 0)),
        'WE': ((0, 0, 0, 0, 0),
               (1, 1, 1, 1, 1),
               (1, 1, 1, 1, 1),
               (1, 1, 1, 1, 1),
               (0, 0, 0, 0, 0)),
        'SN': ((0, 1, 1, 1, 0),
               (0, 1, 1, 1, 0),
               (0, 1, 1, 1, 0),
               (0, 1, 1, 1, 0),
               (0, 1, 1, 1, 0)),
        'SEN': ((0, 1, 1, 1, 1),
                (0, 1, 1, 1, 1),
                (0, 1, 1, 1, 1),
                (0, 1, 1, 1, 1),
                (0, 1, 1, 1, 1)),
        'WEN': ((1, 1, 1, 1, 1),
                (1, 1, 1, 1, 1),
                (1, 1, 1, 1, 1),
                (1, 1, 1, 1, 1),
                (0, 0, 0, 0, 0)),
        'WSN': ((1, 1, 1, 1, 0),
                (1, 1, 1, 1, 0),
                (1, 1, 1, 1, 0),
                (1, 1, 1, 1, 0),
                (1, 1, 1, 1, 0)),
        'WSE': ((0, 0, 0, 0, 0),
                (1, 1, 1, 1, 1),
                (1, 1, 1, 1, 1),
                (1, 1, 1, 1, 1),
                (1, 1, 1, 1, 1)),
        'WSEN': ((1, 1, 1, 1, 1),
                 (1, 1, 1, 1, 1),
                 (1, 1, 1, 1, 1),
                 (1, 1, 1, 1, 1),
                 (1, 1, 1, 1, 1))
    }

    def __init__(self, size):
        self.map = [[Map.GRASS for _ in range(size[1])] for _ in range(size[0])]
        self.size = size

    def set_map_point(self, coords, value):
        if self.is_map_point(coords):
            self.map[coords[0]][coords[1]] = value

    def get_map_point(self, coords):
        if self.is_map_point(coords):
            return self.map[coords[0]][coords[1]]
        return Map.WATER

    def is_map_point(self, coords):
        return 0 <= coords[0] < self.size[0] and 0 <= coords[1] < self.size[1]

    def get_map_point_surroundings(self, coords, map_point_type):
        surroundings = ""
        for i, move in enumerate(Coords.MOVES):
            if map_point_type == self.get_map_point(coords + move):
                surroundings += Coords.DIRECTIONS[i]
        return surroundings

    def fill_to_edge(self, from_coords, direction, value):
        while self.is_map_point(from_coords):
            from_coords += direction
            self.set_map_point(from_coords, value)

    def get_rgb_map(self):
        rgb_map = [[] for _ in range(self.size[0] * Map.SCALING_SIZE)]
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                coords = Coords((j, i))
                surroundings = self.get_map_point_surroundings(
                    coords, self.get_map_point(coords))
                shape = Map.evaluate_shape(
                    surroundings, (Map.GRASS, self.get_map_point(coords)))
                for k in range(Map.SCALING_SIZE):
                    rgb_map[j * Map.SCALING_SIZE + k].extend(shape[k])
        return [Map.COLORS[el] for line in rgb_map for el in line]

    @classmethod
    def evaluate_shape(cls, surroundings, types):
        shape = Map.SHAPES[surroundings]
        return [[types[i] for i in line] for line in shape]

class Coords():

    WEST = 'W'
    SOUTH = 'S'
    EAST = 'E'
    NORTH = 'N'
    DIRECTIONS = (WEST, SOUTH, EAST, NORTH)

    MOVE_WEST = (0, -1)
    MOVE_SOUTH = (1, 0)
    MOVE_EAST = (0, 1)
    MOVE_NORTH = (-1, 0)
    MOVES = (MOVE_WEST, MOVE_SOUTH, MOVE_EAST, MOVE_NORTH)

    def __init__(self, coords):
        self.coords = coords

    def __add__(self, coords):
        return Coords((self.coords[0] + coords[0], self.coords[1] + coords[1]))

    def __iadd__(self, coords):
        return Coords((self.coords[0] + coords[0], self.coords[1] + coords[1]))

    def __getitem__(self, index):
        return self.coords[index]

    def __str__(self):
        return str(self.coords)
