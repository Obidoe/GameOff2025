import pygame
from pygame.math import Vector2
from tower.tower import Tower


# Flamethrower applies dot maybe "Firewall"
class DecreaseTower(Tower):
    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.image.load('images/decrease.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.range = 600
        self.damage = 1
        self.fire_rate = 1
        self.cost = 100
        self.click_pos = None
        self.locked = False
        DecreaseTower.count += 1
        self.index = DecreaseTower.count
        self.wall_pos = None

    def can_shoot(self, current_time):
        return True

    def shoot(self, target, current_time):
        self.last_shot_time = current_time
        self.target_pos = target.rect.center
        self.total_damage += self.damage
        target.health -= self.damage

        print(f'Shooting at {target} dealing {self.damage} damage!')
        print(f'Total damage so far: {self.total_damage}')

    def get_click(self, pos):
        self.click_pos = pos

    def draw(self, screen, current_time):
        # draw sprite
        screen.blit(self.image, self.rect)

        # draw wall
        if self.locked:
            end_pos = self.click_pos
        else:
            end_pos = pygame.mouse.get_pos()
        if abs(self.rect.center[0] - end_pos[0]) <= self.range:
            pygame.draw.line(screen, (180, 0, 0), self.rect.center, end_pos, 3)
            self.wall_pos = (self.rect.center, end_pos)
