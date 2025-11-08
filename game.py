import pygame
import random
import math
import numpy as np
from enemy.enemy import Enemy
from tower.tower import Tower
from map import Map


class Gameloop:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.clock = pygame.time.Clock()

        self.delta_time = 0.1
        self.screen_width = 1280
        self.screen_height = 720
        self.fps = 60

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Algorithm Tower Defense")

        # images
        self.map_png = pygame.image.load('images/map.png').convert()

        self.enemy_image = pygame.image.load('images/testguy.png').convert()
        self.enemy_image.set_colorkey((255, 174, 201))

        self.tower_image = pygame.image.load('images/tower.png').convert()
        self.tower_image.set_colorkey((255, 255, 255))

        self.points = [
            (0, 50),
            (400, 50),
            (400, 460),
            (200, 460),
            (100, 460),
            (100, 670),
            (1280, 670)
        ]

        # init map
        self.tile_size = 64
        grid = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, 0, 0, 0, 0, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 0, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 0, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        ])
        self.map = Map(grid, self.tile_size)

        # Sprite groups
        self.enemy_group = pygame.sprite.Group()

        enemy = Enemy(self.enemy_image, self.map, start_tile=(0, 0))
        self.enemy_group.add(enemy)

        self.tower_group = pygame.sprite.Group()

        self.running = True

    def create_tower(self, mouse_pos):
        if not self.map.place_tower(mouse_pos, self.tower_group):
            return
        tower = Tower(self.tower_image, mouse_pos)
        self.tower_group.add(tower)

    def run(self):
        while self.running:
            # frame rate timing
            self.delta_time = self.clock.tick(self.fps) / 1000
            self.delta_time = max(0.001, min(0.1, self.delta_time))

            # self.screen.blit(self.map_png, (0, 0))
            self.map.draw(self.screen)

            # draw path
            # pygame.draw.lines(self.screen, "red", False, self.points)

            # EVENT HANDLER
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] < self.screen_width and mouse_pos[1] < self.screen_height:
                        self.create_tower(mouse_pos)

            spawn_zone = pygame.Rect(0, 0, 100, 100)
            #pygame.draw.rect(self.screen, (255, 0, 0), spawn_zone)

            goal_zone = pygame.Rect(1180, 620, 100, 100)
            #pygame.draw.rect(self.screen, (0, 255, 0), goal_zone)

            # Update Groups
            self.enemy_group.update()

            # Draw Groups
            self.enemy_group.draw(self.screen)
            self.tower_group.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
