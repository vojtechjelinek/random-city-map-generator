# -*- coding: utf-8 -*-

class Map():

    WATER = 'W'
    GRASS = 'G'
    STREET = 'S'
    COAST = 'C'
    BUILDING1 = 'B1'
    BUILDING2 = 'B2'
    BUILDING3 = 'B3'
    COLORS = {
        WATER: (0, 0, 255),
        GRASS: (0, 180, 0),
        STREET: (50, 50, 50),
        COAST: (194, 178, 128),
        BUILDING1: (150, 150, 150),
        BUILDING2: (170, 170, 170),
        BUILDING3: (190, 190, 190)
    }

    def __init__(self, *size):
        self.map = [[Map.GRASS for _ in range(size[1])] for _ in range(size[0])]
        self.size = size

    def set_map_points(self, coords, value):
        for coord in coords:
            self.set_map_point(coord, value)

    def set_map_point(self, coord, value):
        if self.is_map_point(coord):
            self.map[coord[0]][coord[1]] = value

    def get_map_point(self, coord):
        if self.is_map_point(coord):
            return self.map[coord[0]][coord[1]]
        return Map.WATER

    def is_map_point(self, coord):
        return 0 <= coord[0] < self.size[0] and 0 <= coord[1] < self.size[1]

    def get_map_point_surroundings(self, coords, map_point_type):
        surroundings = ""
        for i, move in enumerate(Coords.MOVES):
            if map_point_type == self.get_map_point(coords + move):
                surroundings += Coords.DIRECTIONS[i]
        return surroundings

    def fill_in_direction(
            self, from_coords, direction, value, n_times=float('inf')):
        while self.is_map_point(from_coords) and n_times > 0:
            self.set_map_point(from_coords, value)
            from_coords += direction
            n_times -= 1

    def get_rgb_map(self):
        return [Map.COLORS[el] for line in self.map for el in line]


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


    def __init__(self, *coords):
        if len(coords) == 1:
            self.coords = coords[0]
        else:
            self.coords = coords

    def __neg__(self):
        return self.get_opposite_direction()

    def __add__(self, coords):
        return Coords(self.coords[0] + coords[0], self.coords[1] + coords[1])

    def __iadd__(self, coords):
        return self.__add__(coords)

    def __sub__(self, coords):
        return Coords(self.coords[0] - coords[0], self.coords[1] - coords[1])

    def __isub__(self, coords):
        return self.__sub__(coords)

    def __mul__(self, factor):
        return Coords(self.coords[0] * factor, self.coords[1] * factor)

    def __rmul__(self, factor):
        return self.__mul__(factor)

    def __imul__(self, factor):
        return self.__mul__(factor)

    def __eq__(self, coords):
        return self.coords[0] == coords[0] and self.coords[1] == coords[1]

    def __getitem__(self, index):
        return self.coords[index]

    def __str__(self):
        return str(self.coords)

    def get_opposite_direction(self):
        return Coords(-self.coords[0], -self.coords[1])

    def get_right_angle_direction(self):
        return Coords(-self.coords[1], self.coords[0])

    @staticmethod
    def get_move_for_symbol(symbol):
        return Coords(Coords.MOVES[Coords.DIRECTIONS.index(symbol)])
