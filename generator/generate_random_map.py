# -*- coding: utf-8 -*-

from pprint import pprint
import random
from PIL import Image

from generator.map import Map, Coords

def is_edge_coords(city_map, coords):
    return not (0 < coords[0] < city_map.size[0] - 1 and
                0 < coords[1] < city_map.size[1] - 1)

def get_random_edge_coords(city_map):
    if random.choice((True, False)):
        part = city_map.size[0] // 5
        rand = random.randrange(part, city_map.size[0] - part)
        return Coords((rand, 0))
    part = city_map.size[1] // 5
    rand = random.randrange(part, city_map.size[1] - part)
    return Coords((0, rand))

def coords_can_river(city_map, next_coords):
    return sum(
        city_map.get_map_point(next_coords + move) == Map.WATER
        for move in Coords.MOVES) == 1

def generate_coast(city_map):
    current_coords = get_random_edge_coords(city_map)
    city_map.set_map_point(current_coords, Map.WATER)

    if current_coords[0] == 0: #north to south
        if current_coords[1] > city_map.size[1] // 2:
            sea_direction = Coords.MOVE_EAST
        else:
            sea_direction = Coords.MOVE_WEST
        from_move = Coords.MOVE_NORTH
        possible_moves = (
            Coords.MOVE_SOUTH, Coords.MOVE_SOUTH, Coords.MOVE_SOUTH,
            Coords.MOVE_WEST, Coords.MOVE_EAST)
        move = Coords.MOVE_SOUTH
    else: #west to east
        if current_coords[0] > city_map.size[0] // 2:
            sea_direction = Coords.MOVE_SOUTH
        else:
            sea_direction = Coords.MOVE_NORTH
        from_move = Coords.MOVE_WEST
        possible_moves = (
            Coords.MOVE_EAST, Coords.MOVE_EAST, Coords.MOVE_EAST,
            Coords.MOVE_NORTH, Coords.MOVE_SOUTH)
        move = Coords.MOVE_EAST

    city_map.fill_to_edge(current_coords, sea_direction, Map.WATER)

    current_coords += move
    city_map.set_map_point(current_coords, Map.WATER)
    city_map.fill_to_edge(current_coords, sea_direction, Map.WATER)

    while True:
        if city_map.get_map_point(current_coords + from_move) == Map.WATER:
            move = random.choice(possible_moves)
            next_coords = current_coords + move
            if coords_can_river(city_map, next_coords):
                current_coords += move
            else:
                move = possible_moves[0]
                current_coords += move
        else:
            move = possible_moves[0]
            current_coords += move

        city_map.set_map_point(current_coords, Map.WATER)
        city_map.fill_to_edge(current_coords, sea_direction, Map.WATER)

        if is_edge_coords(city_map, current_coords):
            break

def generate_streets(city_map):
    block_size = (random.randrange(6, 10), random.randrange(6, 10))
    for i in range(block_size[0], city_map.size[0], block_size[0]):
        for j in range(block_size[1], city_map.size[1], block_size[1]):
            coords = Coords((i, j))
            if city_map.get_map_point(coords) == Map.GRASS:
                city_map.set_map_point(coords, Map.STREET)

    show_image(city_map)
    for i in range(block_size[0], city_map.size[0], block_size[0]):
        block_part_coords = []
        sea_met = False
        for j in range(city_map.size[1]):
            coords = Coords((i, j))
            if city_map.get_map_point(coords) == Map.GRASS:
                block_part_coords.append(coords)
            elif city_map.get_map_point(coords) == Map.STREET:
                if not sea_met:
                    for coords in block_part_coords:
                        city_map.set_map_point(coords, Map.STREET)
                else:
                    sea_met = False
                block_part_coords = []
            elif city_map.get_map_point(coords) == Map.WATER:
                block_part_coords.append(coords)
                sea_met = True
        if not sea_met:
            for coords in block_part_coords:
                city_map.set_map_point(coords, Map.STREET)

    show_image(city_map)
    for i in range(block_size[1], city_map.size[1], block_size[1]):
        block_part_coords = []
        sea_met = False
        for j in range(city_map.size[0]):
            coords = Coords((j, i))
            if city_map.get_map_point(coords) == Map.GRASS:
                block_part_coords.append(coords)
            elif city_map.get_map_point(coords) == Map.STREET:
                if not sea_met:
                    for coords in block_part_coords:
                        city_map.set_map_point(coords, Map.STREET)
                else:
                    sea_met = False
                block_part_coords = []
            elif city_map.get_map_point(coords) == Map.WATER:
                block_part_coords.append(coords)
                sea_met = True
        if not sea_met:
            for coords in block_part_coords:
                city_map.set_map_point(coords, Map.STREET)


def show_image(city_map):
    img = Image.new('RGB',
                    (city_map.size[1] * Map.SCALING_SIZE,
                     city_map.size[0] * Map.SCALING_SIZE))
    img.putdata(city_map.get_rgb_map())
    img.show()

def generate(width, heigth):
    city_map = Map((heigth, width))
    generate_coast(city_map)
    generate_streets(city_map)
    show_image(city_map)
    #pprint(city_map.map)

if __name__ == "__main__":
    generate(200, 100)
