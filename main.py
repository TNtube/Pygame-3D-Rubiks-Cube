import pygame
import OpenGL.GL as GL
import OpenGL.GLU as GLU
import numpy as np
import quaternion
from rubik import Rubik


def main():
    rubik = Rubik(2)
    rotate_slc = {
        pygame.K_1: (0, 0, 1),
        pygame.K_2: (0, 1, 1),
        pygame.K_3: (0, 2, 1),
        pygame.K_4: (1, 0, 1),
        pygame.K_5: (1, 1, 1),
        pygame.K_6: (1, 2, 1),
        pygame.K_7: (2, 0, 1),
        pygame.K_8: (2, 1, 1),
        pygame.K_9: (2, 2, 1),
    }

    init_x = np.radians(25)
    init_y = np.radians(-60)
    q_init = np.quaternion(
        np.cos(init_x / 2), np.sin(init_x / 2), 0, 0
    ) * np.quaternion(
        np.cos(init_y / 2), 0, np.sin(init_y / 2), 0
    )
    q_rot = q_init
    animate = False
    animate_ang = 0
    animate_speed = 5
    rotate = (0, 0, 0)
    running = True
    dragging = False
    last_pos = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not animate and event.key in rotate_slc:
                    animate = True
                    rotate = rotate_slc[event.key]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    last_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    current_pos = pygame.mouse.get_pos()
                    dx = current_pos[0] - last_pos[0]
                    dy = current_pos[1] - last_pos[1]
                    angle_x = np.radians(dy * 0.5)
                    angle_y = np.radians(dx * 0.5)
                    q_drag = np.quaternion(
                        np.cos(angle_x / 2), np.sin(angle_x / 2), 0, 0
                    ) * np.quaternion(np.cos(angle_y / 2), 0, np.sin(angle_y / 2), 0)
                    q_rot = q_drag * q_rot
                    last_pos = current_pos

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslatef(0, 0, -40)

        rot_matrix = quaternion.as_rotation_matrix(q_rot)
        rot_matrix_4x4 = np.eye(4)
        rot_matrix_4x4[:3, :3] = rot_matrix
        GL.glMultMatrixf(rot_matrix_4x4.T)

        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glClearColor(0.2, 0.2, 0.2, 1)

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


if __name__ == "__main__":
    pygame.init()
    display = (1080, 720)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption(
        "Use mouse to rotate the cube, keys from 1 to 9 to rotate each faces"
    )
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GLU.gluPerspective(45, (display[0] / display[1]), 1, 50.0)
    main()
    pygame.quit()
