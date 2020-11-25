import pygame
from rubik import Rubik
from math import radians

AXIS_X, AXIS_Y, AXIS_Z = 0, 1, 2
WHITE = 0xffffff


def main(screen):
    clock = pygame.time.Clock()
    rubik = Rubik(screen)

    rad = radians(3)

    params = {pygame.K_UP: (AXIS_X, -rad),
              pygame.K_DOWN: (AXIS_X, rad),
              pygame.K_LEFT: (AXIS_Y, -rad),
              pygame.K_RIGHT: (AXIS_Y, rad),
              pygame.K_q: (AXIS_Z, -rad),
              pygame.K_d: (AXIS_Z, rad)}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        for key in params:
            if keys[key]:
                for cube in rubik.cubes[2::3]:
                    cube.rotate(*params[key])
        screen.fill(WHITE)

        rubik.draw_shapes()
        pygame.display.flip()
        clock.tick(40)


if __name__ == '__main__':
    pygame.init()
    main(pygame.display.set_mode((450, 450)))
    pygame.quit()
