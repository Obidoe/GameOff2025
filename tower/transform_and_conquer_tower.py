import pygame
from pygame.math import Vector2
from tower.tower import Tower, neon_outline
import math


class TransformTower(Tower):

    slowed = {}
    slow_end_time = {}

    def __init__(self, pos):
        super().__init__(pos)
        raw = pygame.image.load('images/transformtower.png').convert_alpha()
        self.image = neon_outline(raw, color='WHITE', thickness=4)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.range = 100
        self.damage = 3
        self.fire_rate = 1/3
        self.cost = 200
        self.slow = 0.5
        self.slowed_speed = 0
        self.slow_duration = 3
        self.active_blasts = []
        self.blast_radius = 200
        self.blast_zone_time = 5
        self.display_name = 'Quantum Dragfield'

    def shoot(self, target, current_time):
        self.last_shot_time = current_time
        self.target_pos = target.rect.center
        self.total_damage += self.damage
        target.health -= self.damage

        self.active_blasts.append({
            "pos": self.target_pos,
            "time": self.last_shot_time
        })

        print(f'Shooting at {target} dealing {self.damage} damage!')
        print(f'Total damage so far: {self.total_damage}')

    def draw(self, screen, current_time):
        # draw sprite
        screen.blit(self.image, self.rect)

        age = (current_time - self.last_shot_time) / self.shot_display_time
        alpha = int(255 * (1 - age))
        transparent_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        # draw beam
        if self.target_pos and current_time - self.last_shot_time < self.shot_display_time:
            pygame.draw.line(transparent_surface, (156, 240, 233, alpha), self.rect.center, self.target_pos, 6)
            pygame.draw.line(transparent_surface, (170, 255, 255, alpha), self.rect.center, self.target_pos, 4)
            pygame.draw.line(transparent_surface, (190, 255, 255, alpha), self.rect.center, self.target_pos, 2)
            screen.blit(transparent_surface, (0, 0))

    def draw_blast_zone(self, screen, current_time):
        # draw blast radius
        color = (156, 240, 233, 100)

        for blast in self.active_blasts[:]:
            if current_time - blast['time'] < self.blast_zone_time:
                transparent_surface = pygame.Surface((self.blast_radius * 2, self.blast_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(transparent_surface, (156, 240, 255, 200), (self.blast_radius, self.blast_radius),
                                   self.blast_radius+1)
                pygame.draw.circle(transparent_surface, color, (self.blast_radius, self.blast_radius),
                                   self.blast_radius)

                screen.blit(transparent_surface, (blast['pos'][0] - self.blast_radius,
                                                  blast['pos'][1] - self.blast_radius))
            else:
                self.active_blasts.remove(blast)

    def update(self, enemies, current_time):
        if self.placing:
            return
        target = self.detect_enemy(enemies)
        if target and self.can_shoot(current_time):
            self.shoot(target, current_time)

        now = current_time

        # check if enemy is in a blast zone
        for enemy in enemies:
            for blast in self.active_blasts:
                if now - blast['time'] < self.blast_zone_time:
                    dist = Vector2(enemy.rect.center).distance_to(blast['pos'])
                    if dist <= self.blast_radius:
                        if enemy not in TransformTower.slowed:
                            TransformTower.slowed[enemy] = True
                            TransformTower.slow_end_time[enemy] = now + self.slow_duration
                            enemy.speed *= self.slow
                        else:
                            TransformTower.slow_end_time[enemy] = now + self.slow_duration

        # handle slow debuff expiration
        for enemy in list(TransformTower.slowed.keys()):
            if now >= TransformTower.slow_end_time[enemy]:
                del TransformTower.slowed[enemy]
                del TransformTower.slow_end_time[enemy]
                enemy.speed = enemy.base_speed


