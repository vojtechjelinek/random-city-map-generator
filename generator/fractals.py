from svgwrite.drawing import Drawing
import numpy as np

import random

HALF_PI = np.pi / 2
THIRD_OF_PI = np.pi / 3
QUARTER_PI = np.pi / 4

def create_image(filename):
    image = Drawing(filename)
    image.update({"stroke": "black", "stroke_width": 1})
    return image

def create_line(image, coords1, coords2):
    image.add(image.line(coords1, coords2))

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)


def generate_h_tree(depth):
    size = 2 ** depth
    image = create_image("h_tree.svg")
    create_line(image, (size, 0), (size, size))
    h_tree(image, (size, size), size / 2, True)
    image.save()

def h_tree(image, coords, size, horizontal):
    if horizontal:
        new_coords1 = (coords[0] - size, coords[1])
        new_coords2 = (coords[0] + size, coords[1])
    else:
        new_coords1 = (coords[0], coords[1] - size)
        new_coords2 = (coords[0], coords[1] + size)
        size = size / 2

    create_line(image, coords, new_coords1)
    create_line(image, coords, new_coords2)

    if size > 1:
        h_tree(image, new_coords1, size, not horizontal)
        h_tree(image, new_coords2, size, not horizontal)


def generate_binary_tree(depth):
    size = 2 ** depth
    image = create_image("binary_tree.svg")
    create_line(image, (size, 0), (size, 50))
    binary_tree(image, (size, 50), size / 2, True)
    image.save()

def binary_tree(image, coords, size, horizontal):
    if horizontal and size > 1:
        left_coords = (coords[0] - size, coords[1])
        right_coords = (coords[0] + size, coords[1])
        create_line(image, coords, left_coords)
        create_line(image, coords, right_coords)
        binary_tree(image, left_coords, size, not horizontal)
        binary_tree(image, right_coords, size, not horizontal)

    elif size > 1:
        down_coords = (coords[0], coords[1] + random.randrange(25, 75))
        create_line(image, (coords[0], coords[1] - 1), down_coords)

        size = size / 2
        binary_tree(image, down_coords, size, not horizontal)


def generate_pythagoras_tree(depth, size_changes):
    size = 2 ** depth
    image = create_image("pythagoras_tree{}.svg".format(size_changes))
    pythagoras_tree(image, (size + 20, 0), size, HALF_PI, size_changes)
    image.save()

def pythagoras_tree(image, coords, size, angle, size_changes):
    move = pol2cart(size, angle)
    new_coords = (coords[0] + move[0], coords[1] + move[1])
    create_line(image, coords, new_coords)

    if size > 1:
        pythagoras_tree(
            image, new_coords, size / size_changes[0],
            angle + QUARTER_PI, size_changes)
        pythagoras_tree(
            image, new_coords, size / size_changes[1],
            angle - QUARTER_PI, size_changes)


def generate_koch_curve(depth):
    size = 3 ** depth
    image = create_image("koch_curve.svg")
    koch_curve(image, (0, 10), size, 0)
    image.save()

def koch_curve(image, coords, size, angle):
    if size > 1:
        for direction in (0, THIRD_OF_PI, -THIRD_OF_PI):
            koch_curve(image, coords, size/3, angle + direction)
            move = pol2cart(size/3, angle + direction)
            coords = (coords[0] + move[0], coords[1] + move[1])
        koch_curve(image, coords, size/3, angle)

    else:
        move = pol2cart(size, angle)
        new_coords = (coords[0] + move[0], coords[1] + move[1])
        create_line(image, coords, new_coords)


def generate_fractals():
    generate_h_tree(7)
    generate_binary_tree(8)
    generate_pythagoras_tree(7, (1.7, 1.7))
    generate_pythagoras_tree(7, (2.5, 1.2))
    generate_koch_curve(6)

if __name__ == "__main__":
    generate_fractals()
