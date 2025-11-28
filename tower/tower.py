import pygame
from pygame.math import Vector2


def neon_outline(surface, color=(0, 255, 255), thickness=3):
    mask = pygame.mask.from_surface(surface)
    outline_points = mask.outline()

    w, h = surface.get_size()
    result = pygame.Surface((w, h), pygame.SRCALPHA)

    for x, y in outline_points:
        pygame.draw.circle(result, color, (x, y), thickness)

    result.blit(surface, (0, 0))
    return result


class Tower(pygame.sprite.Sprite):
    count = 0

    def __init__(self, pos):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        raw = pygame.image.load('images/MonoRay_Pulse.png').convert_alpha()
        # TESTING COLORS
        self.image = neon_outline(raw, color='WHITE', thickness=4)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.range = 300
        self.damage = 5
        self.total_damage = 0
        self.fire_rate = 2
        self.last_shot_time = 0
        self.target = None
        self.target_pos = None
        self.shot_display_time = 0.15
        self.cost = 100
        Tower.count += 1
        print("TOWER CREATED →", Tower.count)
        self.index = Tower.count
        self.name = f'{self.__class__.__name__}{self.index}'
        self.display_name = f'MonoRay Pulse{self.index}'
        self.placing = True
        self.just_bought = True

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

        # enemy detection (center of hitbox)
#        for enemy in enemies:
#            enemy_pos = Vector2(enemy.rect.center)
#            dist_to_target = tower_pos.distance_to(enemy_pos)
#            if dist_to_target < self.range and dist_to_target < min_dist_to_target:
#                min_dist_to_target = dist_to_target
#                target = enemy
#        return target

    def can_shoot(self, current_time):
        if self.last_shot_time == 0:
            fire_delay = 0
        else:
            fire_delay = 1 / self.fire_rate
        return (current_time - self.last_shot_time) >= fire_delay

    def shoot(self, target, current_time):
        self.last_shot_time = current_time
        self.target_pos = target.rect.center
        self.total_damage += self.damage
        target.health -= self.damage
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
            pygame.draw.line(transparent_surface, (200, 60, 60, alpha), self.rect.center, self.target_pos, 6)
            pygame.draw.line(transparent_surface, (255, 80, 80, alpha), self.rect.center, self.target_pos, 4)
            pygame.draw.line(transparent_surface, (255, 120, 120, alpha), self.rect.center, self.target_pos, 2)
            screen.blit(transparent_surface, (0, 0))

    def update(self, enemies, current_time):
        if self.placing:
            return
        target = self.detect_enemy(enemies)
        if target and self.can_shoot(current_time):
            self.shoot(target, current_time)




