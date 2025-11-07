import pygame
import random
import math
from enemy.enemy import Enemy
from tower.tower import Tower


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
            (100, 650),
            (1280, 670)
        ]

        # Sprite groups
        self.enemy_group = pygame.sprite.Group()
        enemy = Enemy(self.points, self.enemy_image)
        self.enemy_group.add(enemy)

        self.tower_group = pygame.sprite.Group()

        self.running = True

    def create_tower(self, mouse_pos):
        tower = Tower(self.tower_image, mouse_pos)

        # Check if tower overlaps
        for t in self.tower_group:
            if tower.rect.colliderect(t.rect):
                return

        self.tower_group.add(tower)

    def run(self):
        while self.running:
            # frame rate timing
            self.delta_time = self.clock.tick(self.fps) / 1000
            self.delta_time = max(0.001, min(0.1, self.delta_time))

            self.screen.blit(self.map_png, (0, 0))

            # draw path
            pygame.draw.lines(self.screen, "red", False, self.points)

            # EVENT HANDLER
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] < self.screen_width and mouse_pos[1] < self.screen_height:
                        self.create_tower(mouse_pos)

            spawn_zone = pygame.Rect(0, 0, 100, 100)
            pygame.draw.rect(self.screen, (255, 0, 0), spawn_zone)

            goal_zone = pygame.Rect(1180, 620, 100, 100)
            pygame.draw.rect(self.screen, (0, 255, 0), goal_zone)

            # Update Groups
            self.enemy_group.update()

            # Draw Groups
            self.enemy_group.draw(self.screen)
            self.tower_group.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
