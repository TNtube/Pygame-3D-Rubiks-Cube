import pygame
from math import cos, sin
from random import choice

axis_x, axis_y, axis_z = 0, 1, 2

BLACK, WHITE = 0x000, 0xffffff

colors = [*pygame.color.THECOLORS.values()]


def mul_matrix(a, b):
    c = [[0 for _ in range(len(b[0]))] for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            total = 0
            for ii in range(len(a[0])):
                total += a[i][ii] * b[ii][j]
            c[i][j] = total

    return c


def rot_matrix(a, b, t):
    sa, ca = sin(a), cos(a)
    sb, cb = sin(b), cos(b)
    st, ct = sin(t), cos(t)
    return (
        (cb * ct, -cb * st, sb),
        (ca * st + sa * sb * ct, ca * ct - st * sa * sb, -cb * sa),
        (st * sa - ca * sb * ct, ca * st * sb + sa * ct, ca * cb)
    )


class Object:
    def __init__(self, vertices, edges, length):
        self.vertices = vertices
        self.edges = edges
        self.rotation = [3, 3, 0]
        self.len = length

    def rotate(self, axe, o):
        self.rotation[axe] += o

    def polygon(self):
        location = mul_matrix(self.vertices, rot_matrix(*self.rotation))
        return {color: (location[v1], location[v2], location[v3], location[v4])
                for color, (v1, v2, v3, v4) in self.edges.items()}


def point(size, vec, shape):
    return [round(shape.len / 2 * coordinate + frame / 2) for coordinate, frame in zip(vec, size)]


def draw_shape(screen, shape, size):
    pol = shape.polygon()
    for col, points in pol.items():
        pygame.draw.polygon(screen, col, [*(point(size, dot, shape)for dot in points)])


def main(screen):
    clock = pygame.time.Clock()
    size = screen.get_width(), screen.get_height()
    vertices = [(-1, -1, -1), (-1, -1, 1),
                (-1, 1, -1), (-1, 1, 1),
                (1, -1, -1), (1, -1, 1),
                (1, 1, -1), (1, 1, 1)]
    lines = [(0, 1), (0, 2), (2, 3), (1, 3),
             (4, 5), (4, 6), (6, 7), (5, 7),
             (0, 4), (1, 5), (2, 6), (3, 7)]
    choice(colors)

    def pol():
        return {choice(colors): (0, 1, 3, 2), choice(colors): (0, 1, 5, 4),
                choice(colors): (4, 5, 7, 6), choice(colors): (2, 3, 7, 6),
                choice(colors): (0, 4, 6, 2), choice(colors): (1, 5, 7, 3)}

    cubes = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            for k in range(-1, 2):
                vert = [(pos[0] + i * 2, pos[1] + j * 2, pos[2] + k * 2) for pos in vertices]
                if not (i == j == k == 0) and vert not in [obj.vertices for obj in cubes]:
                    cubes.append(Object(vert, pol(), 70))

    rad = 0.05

    params = {pygame.K_UP: (axis_x, -rad),
              pygame.K_DOWN: (axis_x, rad),
              pygame.K_LEFT: (axis_y, -rad),
              pygame.K_RIGHT: (axis_y, rad),
              pygame.K_a: (axis_z, -rad),
              pygame.K_d: (axis_z, rad)}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        for key in params:
            if keys[key]:
                for cube in cubes:
                    cube.rotate(*params[key])
        if keys[pygame.K_w]:
            for cube in cubes:
                cube.len += 5
        if keys[pygame.K_s]:
            for cube in cubes:
                cube.len -= 5
        screen.fill(WHITE)
        for cube in cubes:
            draw_shape(screen, cube, size)
        pygame.display.flip()
        clock.tick(40)


if __name__ == '__main__':
    pygame.init()
    main(pygame.display.set_mode((450, 450)))
    pygame.quit()
