import pygame
import random
import math
from enemy.enemy import Enemy


class Gameloop:

    # pygame setup
    pygame.init()
    clock = pygame.time.Clock()

    delta_time = 0.1
    screen_width = 1280
    screen_height = 720
    fps = 60

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Algorithm Tower Defense")

    # images
    map_png = pygame.image.load('images/map.png').convert()

    enemy_image = pygame.image.load('images/testguy.png').convert()
    enemy_image.set_colorkey((255, 174, 201))

    points = [
        (0, 50),
        (400, 50),
        (400, 460),
        (200, 460),
        (100, 460),
        (100, 650),
        (1150, 650)
    ]

    # Enemy Group
    enemy_group = pygame.sprite.Group()
    enemy = Enemy(points, enemy_image)
    enemy_group.add(enemy)

    running = True
    while running:

        # frame rate timing
        delta_time = clock.tick(fps) / 1000
        delta_time = max(0.001, min(0.1, delta_time))

        screen.blit(map_png, (0, 0))

        # draw path
        pygame.draw.lines(screen, "red", False, points)

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        spawn_zone = pygame.Rect(0, 0, 100, 100)
        pygame.draw.rect(screen, (255, 0, 0), spawn_zone)

        goal_zone = pygame.Rect(1180, 620, 100, 100)
        pygame.draw.rect(screen, (0, 255, 0), goal_zone)

        # Update Groups
        enemy_group.update()

        # Draw Groups
        enemy_group.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

    pygame.quit()
