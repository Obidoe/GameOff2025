import pygame
import random
import math


class Gameloop:

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    delta_time = 0.1

    map_png = pygame.image.load('images/map.png').convert()

    enemy = pygame.image.load('images/testguy.png').convert()
    enemy.set_colorkey((255, 174, 201))

    x = 0
    y = 0
    i = 0
    j = 0
    pnts = [(350, 350), (200, 200), (0, 200), (0, 600), (1100, 550)]
    speed = 100

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.blit(map_png, (0, 0))
        # RENDER YOUR GAME HERE
        spawn_zone = pygame.Rect(0, 0, 100, 100)
        pygame.draw.rect(screen, (255, 0, 0), spawn_zone)

        goal_zone = pygame.Rect(1180, 620, 100, 100)
        pygame.draw.rect(screen, (0, 255, 0), goal_zone)

        screen.blit(enemy, (x, y))

        # flip() the display to put your work on screen
        pygame.display.flip()

        delta_time = clock.tick(60) / 1000
        delta_time = max(0.001, min(0.1, delta_time))

# moves along pnts path
# next is having it choose random points between current position and next position
# moves to chosen points, and continues this until it reaches goal
# make it so it cant move in the wrong direction

        curr_pos = (x, y)
        next_pos = pnts[i]
        random_pos = ()

        if x != pnts[i][j]:

            if x < pnts[i][j]:
                x += math.floor(speed * delta_time)
            if x > pnts[i][j]:
                x -= math.floor(speed * delta_time)

        elif y < pnts[i][j+1]:
            y += math.floor(speed * delta_time)

        else:
            if i < len(pnts) - 1:
                i += 1

        print(f'{(x,y)}')
        print(f'Current Position: {curr_pos}')
        print(f'Next Position: {next_pos}')

    pygame.quit()
