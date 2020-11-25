import pygame
from rubik import Rubik

axis_x, axis_y, axis_z = 0, 1, 2

BLACK, WHITE = 0x000, 0xffffff

colors = pygame.color.THECOLORS


def main(screen):
    clock = pygame.time.Clock()
    rubik = Rubik(screen)

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
                for cube in rubik.cubes[9:-9]:
                    cube.rotate(*params[key])
        screen.fill(WHITE)

        rubik.draw_shapes()
        pygame.display.flip()
        clock.tick(40)


if __name__ == '__main__':
    pygame.init()
    main(pygame.display.set_mode((450, 450)))
    pygame.quit()
