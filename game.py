import pygame
import random
import math
import numpy as np
from enemy.enemy import Enemy
from enemy.enemy2 import Enemy2
from tower.tower import Tower
from map import Map


class Gameloop:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.clock = pygame.time.Clock()
        current_time = pygame.time.get_ticks()

        self.delta_time = 0.1
        self.screen_width = 1280
        self.screen_height = 720
        self.fps = 60

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),
                                              pygame.RESIZABLE | pygame.SCALED)
        pygame.display.set_caption("Algorithm Tower Defense")

        # Waves
        self.waves = {
            1: [5, 0],
            2: [10, 5],
            3: [20, 8],
            4: [20, 12],
            5: [20, 20]
        }
        self.current_wave = 0
        self.wave_delay = 5000
        self.wave_cleared_time = None
        self.wave_waiting = False
        self.game_over = False

        self.spawn_interval = 100
        self.last_enemy_spawn = 0
        self.enemies_left_to_spawn = 0
        self.enemies_to_spawn_random = 0
        self.enemies_to_spawn_bfs = 0

        self.wave_font = pygame.font.SysFont("Arial", 36)

        # images
        self.map_png = pygame.image.load('images/map.png').convert()

        self.enemy_image = pygame.image.load('images/testguy.png').convert()
        self.enemy_image.set_colorkey((255, 174, 201))

        self.tower_image = pygame.image.load('images/tower.png').convert()
        self.tower_image.set_colorkey((255, 255, 255))

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
        self.tower_group = pygame.sprite.Group()

        self.spawn_wave()

        self.running = True

    def spawn_wave(self):
        self.current_wave += 1

        if self.current_wave not in self.waves:
            print('You win!')
            self.game_over = True
            return

        randoms, bfs = self.waves[self.current_wave]
        print(f'Spawning wave {self.current_wave}: {randoms} random pathing enemies and {bfs} BFS enemies!')

        self.enemies_to_spawn_random = randoms
        self.enemies_to_spawn_bfs = bfs
        self.enemies_left_to_spawn = randoms + bfs

        self.last_enemy_spawn = pygame.time.get_ticks()

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
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:  # Example: Exit fullscreen with Escape key
                        self.running = False

                    if event.key == pygame.K_F10:
                        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),
                                                              pygame.FULLSCREEN | pygame.SCALED)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] < self.screen_width and mouse_pos[1] < self.screen_height:
                        self.create_tower(mouse_pos)

            # Draw Groups
            self.enemy_group.draw(self.screen)
            for tower in self.tower_group:
                tower.draw(self.screen)

            # Update Groups
            self.enemy_group.update()
            self.tower_group.update(self.enemy_group)

            # Spawn Waves
            if self.enemies_left_to_spawn > 0:
                now = pygame.time.get_ticks()

                if now - self.last_enemy_spawn >= self.spawn_interval:
                    self.last_enemy_spawn = now
                    self.enemies_left_to_spawn -= 1

                    if self.enemies_to_spawn_random > 0:
                        enemy = Enemy(self.enemy_image, self.map, start_tile=(0, 0))
                        self.enemy_group.add(enemy)
                        self.enemies_to_spawn_random -= 1

                    elif self.enemies_to_spawn_bfs > 0:
                        enemy = Enemy2(self.enemy_image, self.map, start_tile=(0, 0))
                        self.enemy_group.add(enemy)
                        self.enemies_to_spawn_bfs -= 1

            # check if wave complete
            if (self.enemies_left_to_spawn == 0
                    and len(self.enemy_group) == 0
                    and not self.wave_waiting):
                self.wave_waiting = True
                self.wave_cleared_time = pygame.time.get_ticks()

            # wait then start next wave
            if self.wave_waiting:
                now = pygame.time.get_ticks()
                if not self.game_over:
                    wave_clear = self.wave_font.render(f'Wave {self.current_wave} cleared! Waiting for next wave...'
                                                       , True, 'BLACK')
                    self.screen.blit(wave_clear, (600, 600))
                if now - self.wave_cleared_time >= self.wave_delay:
                    self.wave_waiting = False
                    self.spawn_wave()

            pygame.display.flip()

        pygame.quit()
