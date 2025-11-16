import pygame
from pygame.math import Vector2
from tower.tower import Tower


class GreedyTower(Tower):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.image.load('images/greedy_tower.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.range = 400
        self.damage = 6
        self.fire_rate = 1.5
        self.cost = 200

    def shoot(self, target, current_time):
        super().shoot(target, current_time)
        if target.health <= 0:
            target.reward += 20

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
