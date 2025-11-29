import pygame
from pygame.math import Vector2
import random
from collections import deque as qu
from . import greedSearchFunc


class Enemy2(pygame.sprite.Sprite):
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
        self.speed = 2
        self.base_speed = 2
        raw = pygame.image.load('images/enemybfs.png').convert()
        raw.set_colorkey((71, 112, 76))
        self.image = self.neon_outline(raw, color=(255, 255, 0), thickness=2)
        self.rect = self.image.get_rect(center=self.pos)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.damage = 5
        self.max_health = 50
        self.health = self.max_health
        self.reward = 20
        self.dealt_damage = False
        self.name = 'BFS Virus'

    def update(self):
        self.move()
        self.is_alive()

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
        if self.game.lives <= 0 and self.game.killing_blow_enemy is None:
            self.game.killing_blow_enemy = self
        self.dealt_damage = True

    def is_alive(self):
        if self.health <= 0:
            self.kill()
            self.game.gold += self.reward
            print(f'{Enemy2} has died')

    def BFS(self):
        greedM = self.map.grid.copy()
        startpos = (9, 18)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        greed = greedSearchFunc.greedSearchFunc(startpos)
        queue = qu()
        queue.append(greed)
        while queue:
            aroundNode = queue.pop()
            for pos0,pos1 in directions:

                if (aroundNode.starting[0] < greedM.shape[0]-1 and aroundNode.starting[1] < greedM.shape[1]-1 and
                        greedM[aroundNode.starting[0]+pos0, aroundNode.starting[1]+pos1] == 0):
                    Current = greedSearchFunc.greedSearchFunc((aroundNode.starting[0]+pos0, aroundNode.starting[1]+pos1))
                    Current.addDistane(aroundNode.distance + 1)
                    greedM[aroundNode.starting[0]+pos0, aroundNode.starting[1]+pos1] = Current.distance
                    queue.appendleft(Current)
        return greedM

    def move(self):
        global next_dr, next_dc
        mapCopy = self.BFS()
        row, col = self.tile
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        found_move = False
        currentLow = mapCopy[self.tile[0], self.tile[1]]

        for dr,dc in directions:
            if(row+dr < mapCopy.shape[0]-1 and col+dc < mapCopy.shape[1]-1 and currentLow > mapCopy[row+dr,col+dc] and mapCopy[row+dr,col+dc] > -1):
                currentLow = mapCopy[row+dr,col+dc]
                found_move = True
                self.next_tile = (row+dr,col+dc)

        if found_move:
            row, col = self.next_tile
            self.next_pos = Vector2(self.map.tile_to_pix_center(self.next_tile))
            direction = self.next_pos - self.pos
            dist = direction.length()
        else:
            self.attack()
            self.kill()
            print(f'Reached goal!: {self.tile}')
            return

        if dist > self.speed:
            self.pos += direction.normalize() * self.speed

        else:
            self.pos = self.next_pos
            self.prev_tile = self.tile
            self.tile = self.next_tile
            self.next_tile = None

        self.rect.center = self.pos
        found_move = False
