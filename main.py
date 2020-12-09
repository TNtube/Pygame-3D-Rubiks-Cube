import pygame

import OpenGL.GL as GL
import OpenGL.GLU as GLU
from rubik import Rubik


def main(screen):
    rubik = Rubik(3, 2)
    screen.fill(0xffffff)
    rotate_cube = {pygame.K_UP: (-1, 0), pygame.K_DOWN: (1, 0), pygame.K_LEFT: (0, -1), pygame.K_RIGHT: (0, 1)}
    rotate_slc = {
        pygame.K_1: (0, 0, 1), pygame.K_2: (0, 1, 1), pygame.K_3: (0, 2, 1),
        pygame.K_4: (1, 0, 1), pygame.K_5: (1, 1, 1), pygame.K_6: (1, 2, 1),
        pygame.K_7: (2, 0, 1), pygame.K_8: (2, 1, 1), pygame.K_9: (2, 2, 1)
    }

    ang_x, ang_y = 45, -135
    rot_cube = (0, 0)
    animate = False
    animate_ang = 0
    animate_speed = 5
    rotate = (0, 0, 0)
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in rotate_cube:
                    rot_cube = rotate_cube[event.key]
                if not animate and event.key in rotate_slc:
                    animate = True
                    rotate = rotate_slc[event.key]
            if event.type == pygame.KEYUP:
                if event.key in rotate_cube:
                    rot_cube = (0, 0)

        ang_x += rot_cube[0] * 2
        ang_y += rot_cube[1] * 2

        GL.glMatrixMode(GL.GL_MODELVIEW)

        GL.glLoadIdentity()
        GL.glTranslatef(0, 0, -40)
        GL.glRotatef(ang_y, 0, 1, 0)
        GL.glRotatef(ang_x, 1, 0, 0)

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glClearColor(1, 1, 1, 1)

        if animate:
            if animate_ang >= 90:
                for cube in rubik.cubes:
                    cube.update(*rotate)
                animate = False
                animate_ang = 0

        for cube in rubik.cubes:
            cube.draw(cube.polygons, animate, animate_ang, *rotate)
        if animate:
            animate_ang += animate_speed

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    pygame.init()
    display = (1080, 720)
    win = pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GLU.gluPerspective(45, (display[0] / display[1]), 1, 50.0)
    main(win)
    pygame.quit()