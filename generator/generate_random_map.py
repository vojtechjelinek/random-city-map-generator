# -*- coding: utf-8 -*-

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
        return Coords(rand, 0)
    part = city_map.size[1] // 5
    rand = random.randrange(part, city_map.size[1] - part)
    return Coords(0, rand)

def coast_is_straight(prev_moves, move_direction):
    return all(prev_moves[i] == move_direction for i in range(-1, -4, -1))

def create_possible_moves(move_direction, sea_direction):
    curvature = random.randrange(1, 4)
    return ((move_direction, move_direction, move_direction, move_direction) +
            (sea_direction,) * curvature + (-sea_direction,) * (4 - curvature))

def generate_coast(city_map):
    current_coords = get_random_edge_coords(city_map)

    if current_coords[0] == 0: #north to south
        if current_coords[1] > city_map.size[1] // 2:
            sea_direction = Coords(Coords.MOVE_EAST)
        else:
            sea_direction = Coords(Coords.MOVE_WEST)
        move_direction = Coords(Coords.MOVE_SOUTH)
    else: #west to east
        if current_coords[0] > city_map.size[0] // 2:
            sea_direction = Coords(Coords.MOVE_SOUTH)
        else:
            sea_direction = Coords(Coords.MOVE_NORTH)
        move_direction = Coords(Coords.MOVE_EAST)

    possible_moves = create_possible_moves(move_direction, sea_direction)

    prev_moves = [sea_direction, sea_direction, sea_direction]
    while True:
        city_map.fill_in_direction(current_coords, sea_direction, Map.WATER)
        city_map.fill_in_direction(
            current_coords, -sea_direction, Map.COAST, 4)

        if coast_is_straight(prev_moves, move_direction):
            move = random.choice(possible_moves)
        else:
            move = possible_moves[0]

        prev_moves.append(move)
        current_coords += move

        if is_edge_coords(city_map, current_coords):
            city_map.fill_in_direction(current_coords, sea_direction, Map.WATER)
            city_map.fill_in_direction(
                (current_coords - sea_direction), -sea_direction, Map.COAST, 4)
            break

def generate_intersections(city_map, block_size):
    for i in range(block_size[0], city_map.size[0], block_size[0]):
        for j in range(block_size[1], city_map.size[1], block_size[1]):
            coords = Coords(i, j)
            if city_map.get_map_point(coords) == Map.GRASS:
                city_map.set_map_point(coords, Map.STREET)

def generate_streets(city_map, block_size, vertical):
    block_lenght = block_size[int(vertical)]
    map_length = city_map.size[int(vertical)]
    for i in range(block_lenght, map_length, block_lenght):
        block_part_coords = []
        sea_met = False
        for j in range(city_map.size[int(not vertical)]):
            if vertical:
                coords = Coords(j, i)
            else:
                coords = Coords(i, j)

            if city_map.get_map_point(coords) == Map.GRASS:
                block_part_coords.append(coords)
            elif city_map.get_map_point(coords) == Map.STREET:
                if not sea_met:
                    city_map.set_map_points(block_part_coords, Map.STREET)
                else:
                    sea_met = False
                block_part_coords = []
            elif not city_map.get_map_point(coords) == Map.GRASS:
                block_part_coords.append(coords)
                sea_met = True

        if not sea_met:
            city_map.set_map_points(block_part_coords, Map.STREET)


def generate_street_grid(city_map):
    choice = random.random()
    if choice > 0.66: #choose grid shape
        block_size = (random.randrange(12, 16), random.randrange(24, 32))
    elif choice > 0.33:
        block_size = (random.randrange(24, 32), random.randrange(12, 16))
    else:
        block_size = (random.randrange(12, 16), random.randrange(12, 16))

    generate_intersections(city_map, block_size)
    generate_streets(city_map, block_size, True)
    generate_streets(city_map, block_size, False)


def create_building(city_map, coords, street_directions):
    building_points = []
    building_size = (random.randrange(3, 6), random.randrange(3, 6))
    for i in range(building_size[0]):
        for j in range(building_size[1]):
            building_points.append(
                coords + (street_directions[0] * i) +
                (street_directions[1] * j))
    if all(city_map.get_map_point(building_point) == Map.GRASS
           for building_point in building_points): #whole building is on grass
        building_type = (
            random.choice((Map.BUILDING1, Map.BUILDING2, Map.BUILDING3)))
        city_map.set_map_points(building_points, building_type)

def generate_corner_building(city_map, coords):
    surrounding_streets = (
        city_map.get_map_point_surroundings(coords, Map.STREET))
    point_type = city_map.get_map_point(coords)
    if len(surrounding_streets) == 2 and point_type == Map.GRASS:
        building_directions = (
            -Coords.get_move_for_symbol(surrounding_streets[0]),
            -Coords.get_move_for_symbol(surrounding_streets[1]))
        create_building(city_map, coords, building_directions)

def generate_normal_building(city_map, coords):
    surrounding_streets = (
        city_map.get_map_point_surroundings(coords, Map.STREET))
    point_type = city_map.get_map_point(coords)
    if len(surrounding_streets) == 1 and point_type == Map.GRASS:
        street_direction = Coords.get_move_for_symbol(surrounding_streets)
        building_directions = (
            -street_direction,
            -street_direction.get_right_angle_direction())
        create_building(city_map, coords, building_directions)

def generate_buildings(city_map):
    for i in range(city_map.size[0]):
        for j in range(city_map.size[1]):
            generate_corner_building(city_map, Coords(i, j))
    for i in range(city_map.size[0]):
        for j in range(city_map.size[1]):
            generate_normal_building(city_map, Coords(i, j))

def save_image(city_map, filename):
    img = Image.new('RGB', (city_map.size[1], city_map.size[0]))
    img.putdata(city_map.get_rgb_map())
    img = img.resize((2 * city_map.size[1], 2 * city_map.size[0]))
    img.save(filename)

def generate(width, heigth):
    city_map = Map(heigth, width)
    generate_coast(city_map)
    generate_street_grid(city_map)
    generate_buildings(city_map)
    save_image(city_map, "map.png")

if __name__ == "__main__":
    generate(400, 400)
