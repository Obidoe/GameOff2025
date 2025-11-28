import pygame
from pygame.math import Vector2
from . import aSearch
from map import towerLoc
import random
from collections import deque as qu



class Enemy3(pygame.sprite.Sprite):
    def __init__(self, game_map, game, start_tile):
        pygame.sprite.Sprite.__init__(self)
        self.map = game_map
        self.game = game
        self.start_tile = start_tile
        self.tile = self.start_tile
        self.pos = Vector2(self.map.tile_to_pix_center(self.tile))
        self.prev_tile = None
        self.next_tile = None
        self.next_pos = None
        self.Directions = aSearch.aSearc(self.map.grid,self.start_tile,(10, 19), towerLoc)
        self.speed = 3
        self.base_speed = 3
        raw = pygame.image.load('images/enemyastar.png').convert()
        raw.set_colorkey((71, 112, 76))
        self.image = self.neon_outline(raw, color=(255, 0, 255), thickness=2)
        self.rect = self.image.get_rect(center=self.pos)
        self.rect.center = self.pos
        self.damage = 5
        self.max_health = 100
        self.health = self.max_health
        self.reward = 20

    @staticmethod
    def neon_outline(surface, color=(0, 255, 255), thickness=3):
        mask = pygame.mask.from_surface(surface)
        outline_points = mask.outline()

        w, h = surface.get_size()
        result = pygame.Surface((w, h), pygame.SRCALPHA)

        for x, y in outline_points:
            pygame.draw.circle(result, color, (x, y), thickness)

        result.blit(surface, (0, 0))
        return result

    def update(self):
        self.move()
        self.is_alive()

    def draw(self, screen):
        # draw sprite
        screen.blit(self.image, self.rect)
        health_bar_length = 64
        health_bar_width = 10

        # draw damage
        hp_as_percentage = self.health / self.max_health
        pygame.draw.rect(screen, (190, 0, 0), (self.pos.x - health_bar_length / 2, self.pos.y - 50,
                                               health_bar_length, health_bar_width))

        # draw health bar
        pygame.draw.rect(screen, (0, 190, 0), (self.pos.x - health_bar_length / 2, self.pos.y - 50,
                                               health_bar_length * hp_as_percentage, health_bar_width))

    def attack(self):
        self.game.lives -= self.damage

    def is_alive(self):
        if self.health <= 0:
            self.kill()
            self.game.gold += self.reward
            print(f'{Enemy3} has died')


    def move(self):
        # If no current target, load next tile from the path
        if self.next_tile is None:
            if not self.Directions:  # Path empty → reached goal
                self.attack()
                self.kill()
                print(f"Reached goal!")
                return

            self.next_tile = self.Directions.pop(0)
            self.next_pos = Vector2(self.map.tile_to_pix_center(self.next_tile))

        # Move toward next_pos gradually
        direction = self.next_pos - self.pos
        dist = direction.length()

        if dist > self.speed:
            # move toward target
            self.pos += direction.normalize() * self.speed
        else:
            # Snap to tile
            self.pos = self.next_pos
            self.prev_tile = self.tile
            self.tile = self.next_tile
            self.next_tile = None  # ← allow next pop on next frame

        self.rect.center = self.pos
