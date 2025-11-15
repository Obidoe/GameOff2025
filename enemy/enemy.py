import pygame
from pygame.math import Vector2
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, game_map, game, start_tile):
        pygame.sprite.Sprite.__init__(self)
        self.map = game_map
        self.game = game
        self.start_tile = start_tile
        self.tile = self.start_tile
        self.pos = Vector2(self.map.tile_to_pix_center(self.tile))
        self.prev_tile = None
        self.next_tile = None
        self.next_pos = None
        self.speed = 10
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.damage = 10
        self.max_health = 20
        self.health = self.max_health

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
            print(f'{Enemy} has died')

    # This will be where the different algorithms go
    # Right now its random
    def move(self):

        if self.next_tile is None:
            # Part 1: Choose Direction
            row, col = self.tile
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)
            found_move = False

            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.map.grid.shape[0] and 0 <= nc < self.map.grid.shape[1]:
                    if self.map.grid[nr, nc] == 0 and (nr, nc) != self.prev_tile:
                        self.next_tile = (nr, nc)
                        self.next_pos = Vector2(self.map.tile_to_pix_center(self.next_tile))
                        found_move = True
                        break
            # Can't find a tile to move to (Either back at the start or at the end)
            # This tests if it is at the start
            if not found_move:
                if self.tile == self.start_tile:
                    self.next_tile = self.start_tile
                    self.next_pos = Vector2(self.map.tile_to_pix_center(self.next_tile))
                    found_move = True
            # If it still can't find a move, then it is probably at the end.
            if not found_move:
                self.attack()
                self.kill()
                print(f'Reached goal!: {self.tile}')
                return

        if self.next_pos is None:
            return

        # Part 2: Movement
        direction = self.next_pos - self.pos
        dist = direction.length()

        if dist > self.speed:
            self.pos += direction.normalize() * self.speed
        else:
            self.pos = self.next_pos
            self.prev_tile = self.tile
            self.tile = self.next_tile
            self.next_tile = None

        self.rect.center = self.pos
