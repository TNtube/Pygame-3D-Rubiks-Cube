import pygame
import OpenGL.GL as GL

COLORS = {key: tuple(value[:3]) for key, value in pygame.color.THECOLORS.items()}


class Cube(object):
    edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7),
    )
    polygons = (
        (0, 1, 2, 3),
        (3, 2, 7, 6),
        (6, 7, 5, 4),
        (4, 5, 1, 0),
        (1, 5, 7, 2),
        (4, 0, 3, 6),
    )
    vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1),
    )
    colors = (
        COLORS["blue"],
        (1, 0.5, 0),# orange
        COLORS["green"],
        COLORS["red"],
        COLORS["white"],
        COLORS["yellow"],
    )

    def __init__(self, ident: tuple, n: int, scale: int) -> None:
        self.n = n
        self.scale = scale
        self.current = [*ident]
        self.rot = [[1 if i == j else 0 for i in range(3)] for j in range(3)]

    def is_affected(self, axis: int, slc: int):
        return self.current[axis] == slc

    def update(self, axis: int, slc: int, dr: int):

        if not self.is_affected(axis, slc):
            return

        i = (axis + 1) % 3
        j = (axis + 2) % 3
        for k in range(3):
            self.rot[k][i], self.rot[k][j] = -self.rot[k][j] * dr, self.rot[k][i] * dr

        self.current[i], self.current[j] = (
            self.current[j] if dr < 0 else self.n - 1 - self.current[j],
            self.current[i] if dr > 0 else self.n - 1 - self.current[i],
        )

    def transform_matrix(self):
        s_a = [[s * self.scale for s in a] for a in self.rot]
        s_t = [(p - (self.n - 1) / 2) * 2 * self.scale for p in self.current]
        return [*s_a[0], 0, *s_a[1], 0, *s_a[2], 0, *s_t, 1]

    def draw(self, surf, animate, angle, axis, slc, dr):

        GL.glPushMatrix()
        if animate and self.is_affected(axis, slc):
            GL.glRotatef(angle * dr, *[1 if i == axis else 0 for i in range(3)])
        GL.glMultMatrixf(self.transform_matrix())

        GL.glBegin(GL.GL_QUADS)
        for i in range(len(surf)):
            GL.glColor3fv(Cube.colors[i])
            for j in surf[i]:
                GL.glVertex3fv(Cube.vertices[j])
        GL.glEnd()

        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glLineWidth(3)
        GL.glDisable(GL.GL_LINE_SMOOTH)

        GL.glBegin(GL.GL_LINES)
        GL.glColor3fv((0, 0, 0))
        for edge in Cube.edges:
            for vertex in edge:
                GL.glVertex3fv(Cube.vertices[vertex])
        GL.glEnd()
        GL.glPopMatrix()


class Rubik:
    def __init__(self, scale):
        self.n = 3
        cr = range(self.n)
        self.scale = scale
        self.cubes = self.init_cube(cr)

    def init_cube(self, cr):
        cubes = []
        for z in cr:
            for y in cr:
                for x in cr:
                    cubes.append(Cube((x, y, z), self.n, self.scale))
        return cubes
