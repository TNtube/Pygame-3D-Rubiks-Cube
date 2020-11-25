from __future__ import annotations
import pygame
from numpy import dot
from utils import average_z, rot_matrix, fit_point
from math import radians

COLORS = pygame.color.THECOLORS
BLACK = 0x000000


class Object:
    def __init__(self, vertices: list[tuple, tuple], edges: list[tuple], length: int, size: tuple):
        self.vertices = vertices
        self.edges = edges
        self.rotation = [radians(45), radians(45), 0]
        self.movement = [size[0], size[1], length]
        self.location = vertices

    def rotate(self, axe: int, o: int) -> None:
        self.rotation[axe] += o

    def polygon(self) -> list[tuple[tuple, tuple]]:
        self.location = dot(self.vertices, rot_matrix(*self.rotation))
        return [(color, (self.location[v1], self.location[v2], self.location[v3], self.location[v4]))
                for color, (v1, v2, v3, v4) in self.edges]


class Rubik:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.size = screen.get_width(), screen.get_height()
        self.vertices = [(-1, -1, -1), (-1, -1, 1),
                         (-1, 1, -1), (-1, 1, 1),
                         (1, -1, -1), (1, -1, 1),
                         (1, 1, -1), (1, 1, 1)]
        self.polygons = [(COLORS["blue"], (0, 1, 3, 2)), (COLORS["yellow"], (0, 1, 5, 4)),
                         (COLORS["green"], (4, 5, 7, 6)), (COLORS["white"], (2, 3, 7, 6)),
                         (COLORS["orange"], (0, 4, 6, 2)), (COLORS["red"], (1, 5, 7, 3))]
        self.cubes = self.init_cube()
        self.faces = {"x": {}, "y": {}, "z": {}}

    def init_cube(self) -> list[Object]:
        cubes = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    vert = [(pos[0] + i * 2, pos[1] + j * 2, pos[2] + k * 2) for pos in self.vertices]
                    cubes.append(Object(vert, self.polygons, 70, self.size))
        return cubes

    def draw_shapes(self) -> None:
        pol = []
        for shape in self.cubes:
            polygon = shape.polygon()
            pol.extend(polygon)
        pol.sort(key=lambda p: average_z(p[1]))

        for col, points in pol:
            po = list((fit_point(point, self.cubes[0])for point in points))
            pygame.draw.polygon(self.screen, col, po)
            pygame.draw.polygon(self.screen, BLACK, po, 3)
