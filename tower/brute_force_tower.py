import pygame
from pygame.math import Vector2
from tower.tower import Tower
import random
import math


class BruteForce(Tower):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.image.load('images/brute_force.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.range = 200
        self.damage = 2
        self.fire_rate = 1
        self.cost = 100
        self.spread_angle = 60
        self.projectiles = 8
        self.shot_lines = []

    # Nearest Enemy
    def detect_enemy(self, enemies):
        target = None
        min_dist_to_target = float('inf')
        tower_pos = Vector2(self.rect.center)

        # enemy detection (entire hitbox)
        for enemy in enemies:
            enemy_rect = enemy.rect
            closest_x = max(enemy_rect.left, min(tower_pos.x, enemy_rect.right))
            closest_y = max(enemy_rect.top, min(tower_pos.y, enemy_rect.bottom))
            closest_point = Vector2(closest_x, closest_y)
            dist_to_target = tower_pos.distance_to(closest_point)
            if dist_to_target < self.range and dist_to_target < min_dist_to_target:
                min_dist_to_target = dist_to_target
                target = enemy
        return target

    def shoot(self, target, current_time):

        self.last_shot_time = current_time
        self.shot_lines = []

        tower_pos = Vector2(self.rect.center)
        target_pos = Vector2(target.rect.center)

        direction = target_pos - tower_pos
        base_angle = math.atan2(direction.y, direction.x)

        for bullet in range(self.projectiles):
            # shotgun spread effect
            offset = math.radians(random.uniform(-self.spread_angle/2, self.spread_angle/2))
            bullet_angle = base_angle + offset

            bullet_target = tower_pos + Vector2(math.cos(bullet_angle) * self.range,
                                                math.sin(bullet_angle) * self.range)

            self.shot_lines.append((tower_pos, bullet_target))
            target.health -= self.damage

    def draw(self, screen, current_time):
        super().draw(screen, current_time)
        if current_time - self.last_shot_time < self.shot_display_time:
            for start, end in self.shot_lines:
                pygame.draw.line(screen, (255, 50, 50), start, end, 3)

