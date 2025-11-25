import pygame
import random
import math
import numpy as np
from enemy.enemy import Enemy
from enemy.enemy2 import Enemy2
from tower.tower import Tower
from tower.brute_force_tower import BruteForce
from tower.greedy_tower import GreedyTower
from tower.decrease_and_conquer_tower import DecreaseTower
from tower.transform_and_conquer_tower import TransformTower
from tower.divide_and_conquer_tower import DivideTower
from map import Map
from menu import Menu


class Gameloop:
    def __init__(self):
        # pygame setup
        pygame.init()
        self.clock = pygame.time.Clock()
        self.current_time = 0
        self.game_time = 0

        self.delta_time = 0.1
        self.screen_width = 1580
        self.screen_height = 720
        self.fps = 60

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),
                                              pygame.RESIZABLE | pygame.SCALED)
        pygame.display.set_caption("Algorithm Tower Defense")

        # pause after wave
        self.game_pause = True
        # pause when press 'esc'
        self.menu_pause = False

        # Side Panel Menu
        self.menu = Menu(self)

        # Player
        self.lives = 100
        self.gold = 200

        # Tower Management
        self.selected_tower = None

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

        self.big_font = pygame.font.SysFont("Arial", 144)
        self.medium_font = pygame.font.SysFont("Arial", 77)
        self.small_font = pygame.font.SysFont("Arial", 36)
        self.very_small_font = pygame.font.SysFont("Arial", 12)
        self.auto_size = max(12, int(self.screen_width * 0.02))
        self.auto_font = pygame.font.SysFont("Arial", self.auto_size)

        # images
        self.map_png = pygame.image.load('images/map.png').convert()

        self.pause_button_image = pygame.image.load('images/pause_button.png').convert()

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

    def toggle_game_pause(self):
        self.game_pause = not self.game_pause

    def spawn_wave(self):
        self.current_wave += 1

        if self.current_wave not in self.waves:
            # win
            self.game_over = True
            return

        randoms, bfs = self.waves[self.current_wave]
        print(f'Spawning wave {self.current_wave}: {randoms} random pathing enemies and {bfs} BFS enemies!')

        self.enemies_to_spawn_random = randoms
        self.enemies_to_spawn_bfs = bfs
        self.enemies_left_to_spawn = randoms + bfs

        self.last_enemy_spawn = pygame.time.get_ticks()

    def create_tower(self, mouse_pos, tower_type):

        if self.selected_tower and self.selected_tower.placing:
            self.delete_tower()

        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()

        tower = tower_type(mouse_pos)
        if self.gold >= tower.cost:
            tower.placing = True
            self.selected_tower = tower
            self.menu.set_selected_tower(tower)
            self.tower_group.add(tower)
            tower.just_bought = True

    def select_tower(self, mouse_pos):
        for tower in self.tower_group:
            if tower.rect.collidepoint(mouse_pos):
                self.selected_tower = tower
                self.menu.set_selected_tower(tower)
                break
            else:
                self.selected_tower = None
                self.menu.set_selected_tower(None)

    def delete_tower(self):
        self.tower_group.remove(self.selected_tower)
        self.selected_tower = None

    def event_handler(self):
        for event in pygame.event.get():

            self.menu.handle_event(event)
            if self.menu.event_consumed:
                continue

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.menu_pause = not self.menu_pause

                if event.key == pygame.K_F10:
                    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),
                                                          pygame.FULLSCREEN | pygame.SCALED)

                if event.key == pygame.K_p:
                    self.game_pause = False

            if not self.menu_pause and not self.game_over:
                mouse_pos = pygame.mouse.get_pos()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.create_tower(mouse_pos, Tower)
                    if event.key == pygame.K_2:
                        self.create_tower(mouse_pos, BruteForce)
                    if event.key == pygame.K_3:
                        self.create_tower(mouse_pos, DecreaseTower)
                    if event.key == pygame.K_4:
                        self.create_tower(mouse_pos, GreedyTower)
                    if event.key == pygame.K_5:
                        self.create_tower(mouse_pos, TransformTower)
                    if event.key == pygame.K_6:
                        self.create_tower(mouse_pos, DivideTower)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_pos[0] < self.screen_width and mouse_pos[1] < self.screen_height:

                        if event.button == 1:
                            print(self.selected_tower)

                            if self.selected_tower and self.selected_tower.placing:
                                tower = self.selected_tower
                                mouse_pos = pygame.mouse.get_pos()

                                if tower.__class__.__name__ == 'DecreaseTower':
                                    tower.locked = False

                                if self.map.place_tower(mouse_pos, self.tower_group, ignore_tower=tower):
                                    tower.placing = False
                                    tower.rect.center = mouse_pos

                                    if getattr(tower, 'just_bought', False):
                                        self.gold -= tower.cost
                                        tower.just_bought = False
                                return

                            if self.selected_tower.__class__.__name__ == 'DecreaseTower' \
                                    and not self.selected_tower.locked:
                                self.selected_tower.get_click(mouse_pos)
                                self.selected_tower.locked = True

                            self.select_tower(mouse_pos)

    def update_running(self):
        # Update side panel
        self.menu.update(pygame.mouse.get_pos())

        # Update Groups
        self.enemy_group.update()
        DecreaseTower.did_tick_this_frame = False
        self.tower_group.update(self.enemy_group, self.current_time)

        # Spawn Waves
        if self.enemies_left_to_spawn > 0:
            now = pygame.time.get_ticks()

            if now - self.last_enemy_spawn >= self.spawn_interval:
                self.last_enemy_spawn = now
                self.enemies_left_to_spawn -= 1

                if self.enemies_to_spawn_random > 0:
                    enemy = Enemy(self.map, self, start_tile=(0, 0))
                    self.enemy_group.add(enemy)
                    self.enemies_to_spawn_random -= 1

                elif self.enemies_to_spawn_bfs > 0:
                    enemy = Enemy2(self.map, self, start_tile=(0, 0))
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
                wave_clear_text = self.big_font.render(f'Wave {self.current_wave} 'f'cleared!', True,
                                                                 'WHITE')
                wave_clear_rect = wave_clear_text.get_rect(center=(self.screen_width / 2 - 150, self.screen_height / 2))
                self.screen.blit(wave_clear_text, wave_clear_rect)
            if now - self.wave_cleared_time >= self.wave_delay:
                self.wave_waiting = False
                self.game_pause = True
                self.spawn_wave()

        # check if player has any lives left
        if self.lives <= 0:
            self.game_over = True

        # if player wins
        if self.lives > 0 and self.game_over:
            game_over_text = self.big_font.render(f'YOU WIN', True, 'WHITE')
            game_over_text_rect = game_over_text.get_rect(center=(self.screen_width / 2 - 150, self.screen_height / 2))
            self.screen.blit(game_over_text, game_over_text_rect)

    def run(self):

        while self.running:

            # frame rate timing
            self.delta_time = self.clock.tick(self.fps) / 1000
            self.delta_time = max(0.001, min(0.1, self.delta_time))

            # draw map
            self.map.draw(self.screen)

            # draw transform blast zones UNDER everything else
            for tower in self.tower_group:
                if tower.placing:
                    tower.rect.center = pygame.mouse.get_pos()
                if isinstance(tower, TransformTower):
                    tower.draw_blast_zone(self.screen, self.current_time)

            # event handler
            self.event_handler()

            # Draw Groups
            for enemy in self.enemy_group:
                enemy.draw(self.screen)
            for tower in self.tower_group:
                tower.draw(self.screen, self.current_time)

            # Draw Selected
            if self.selected_tower:
                t = self.selected_tower
                pygame.draw.rect(self.screen, (255, 0, 0),
                                 (t.rect.x - 5, t.rect.y - 5, t.rect.width + 10, t.rect.height + 10), width=2)

                # draw radius
                color = (255, 0, 0, 160)
                transparent_surface = pygame.Surface((t.range * 2, t.range * 2), pygame.SRCALPHA)
                pygame.draw.circle(transparent_surface, color, (t.range, t.range), t.range, width=2)
                self.screen.blit(transparent_surface, (t.rect.centerx - t.range, t.rect.centery - t.range))

            self.menu.update(pygame.mouse.get_pos())
            self.menu.draw(self.screen)

            # Game paused via menu
            if self.menu_pause:
                pause_text = self.big_font.render(f'PAUSED', True, 'WHITE')
                pause_rect = pause_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
                self.screen.blit(pause_text, pause_rect)
                pygame.display.flip()
                continue

            # Game paused after wave
            if self.game_pause and not self.game_over:
                pygame.display.flip()
                continue

            # Game over!
            if self.game_over and self.lives <= 0:
                game_over_text = self.big_font.render(f'GAME OVER', True, 'WHITE')
                game_over_text_rect = game_over_text.get_rect(center=(self.screen_width / 2 - 150, self.screen_height / 2))
                self.screen.blit(game_over_text, game_over_text_rect)
                pygame.display.flip()
                continue

            # Game not paused
            else:
                self.update_running()
                self.current_time += self.delta_time

            pygame.display.flip()

        pygame.quit()
