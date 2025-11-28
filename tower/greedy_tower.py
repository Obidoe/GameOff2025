import pygame
from pygame.math import Vector2
from tower.tower import Tower, neon_outline


class GreedyTower(Tower):
    def __init__(self, pos):
        super().__init__(pos)
        raw = pygame.image.load('images/greedy_tower.png').convert_alpha()
        self.image = neon_outline(raw, color='WHITE', thickness=4)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.range = 400
        self.damage = 6
        self.fire_rate = 1.5
        self.cost = 300
        self.gold_earned = 0
        GreedyTower.count += 1
        self.index = GreedyTower.count
        self.display_name = 'GreedCore Extractor'

    def shoot(self, target, current_time):
        super().shoot(target, current_time)
        if target.health <= 0:
            target.reward += 20
            self.gold_earned += 20
            print(f'Gold earned from greedy: {self.gold_earned}')

    def detect_enemy(self, enemies):
        target = None
        min_hp = float('inf')
        tower_pos = Vector2(self.rect.center)

        # enemy detection (entire hitbox)
        for enemy in enemies:
            enemy_rect = enemy.rect
            closest_x = max(enemy_rect.left, min(tower_pos.x, enemy_rect.right))
            closest_y = max(enemy_rect.top, min(tower_pos.y, enemy_rect.bottom))
            closest_point = Vector2(closest_x, closest_y)
            dist_to_target = tower_pos.distance_to(closest_point)
            if dist_to_target < self.range and enemy.health < min_hp:
                min_hp = enemy.health
                target = enemy
        return target

    def draw(self, screen, current_time):
        # draw sprite
        screen.blit(self.image, self.rect)

        age = (current_time - self.last_shot_time) / self.shot_display_time
        alpha = int(255 * (1 - age))
        transparent_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        # draw beam
        if self.target_pos and current_time - self.last_shot_time < self.shot_display_time:
            pygame.draw.line(transparent_surface, (60, 200, 60, alpha), self.rect.center, self.target_pos, 6)
            pygame.draw.line(transparent_surface, (80, 255, 80, alpha), self.rect.center, self.target_pos, 4)
            pygame.draw.line(transparent_surface, (120, 255, 120, alpha), self.rect.center, self.target_pos, 2)
            screen.blit(transparent_surface, (0, 0))
