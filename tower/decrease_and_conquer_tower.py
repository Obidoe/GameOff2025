import pygame
from pygame.math import Vector2
from tower.tower import Tower
import math


# Flamethrower applies dot maybe "Firewall"
class DecreaseTower(Tower):
    dot_stacks = {}
    dot_start_time = {}
    dot_end_time = {}
    dot_cooldown = {}
    did_tick_this_frame = False

    def __init__(self, pos):
        super().__init__(pos)
        self.image = pygame.image.load('images/decrease.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.range = 600
        self.damage = 1
        self.dot_duration = 3
        self.fire_rate = 0.5
        self.dot_stack_cd = {}
        self.cost = 100
        self.click_pos = None
        self.locked = False
        DecreaseTower.count += 1
        self.index = DecreaseTower.count
        self.wall_pos = None
        self.end_pos = None

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

    def point_line_distance(self, px, py, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:
            return math.hypot(px - x1, py - y1)

        t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)

        t = max(0, min(1, t))

        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        return math.hypot(px - closest_x, py - closest_y)

    def draw(self, screen, current_time):
        # draw sprite
        screen.blit(self.image, self.rect)

        # draw wall
        if self.locked:
            self.end_pos = self.click_pos
        else:
            self.end_pos = pygame.mouse.get_pos()

        x, y = self.rect.center
        mx, my = self.end_pos

        dx = mx - x
        dy = my - y
        dist = math.hypot(dx, dy)

        if dist > self.range:
            scale = self.range / dist
            mx = x + dx * scale
            my = y + dy * scale

        self.end_pos = (mx, my)

        pygame.draw.line(screen, (180, 0, 0), self.rect.center, self.end_pos, 3)
        self.wall_pos = (self.rect.center, self.end_pos)

    def update(self, enemies, current_time):
        for enemy in enemies:
            ex, ey = enemy.rect.center
            radius = enemy.rect.width / 2
            dist = self.point_line_distance(ex, ey, self.rect.center[0], self.rect.center[1],
                                            self.end_pos[0], self.end_pos[1])

            if dist < radius:

                now = current_time
                # Handling enemy / DOT status

                if enemy not in self.dot_stack_cd:
                    self.dot_stack_cd[enemy] = 0

                if enemy not in DecreaseTower.dot_stacks:
                    DecreaseTower.dot_stacks[enemy] = 0
                    DecreaseTower.dot_start_time[enemy] = 0
                    DecreaseTower.dot_end_time[enemy] = 0
                    DecreaseTower.dot_cooldown[enemy] = 0

                if now >= self.dot_stack_cd[enemy]:
                    DecreaseTower.dot_stacks[enemy] += 1
                    self.dot_stack_cd[enemy] = now + 1
                    DecreaseTower.dot_start_time[enemy] = now
                    DecreaseTower.dot_end_time[enemy] = now + self.dot_duration
                    DecreaseTower.dot_cooldown[enemy] = now + self.fire_rate

        # This only applies DOT to enemies with stacks
        now = current_time

        if DecreaseTower.did_tick_this_frame:
            return

        for enemy in list(DecreaseTower.dot_stacks.keys()):

            print(DecreaseTower.dot_stacks[enemy])

            if now >= DecreaseTower.dot_end_time[enemy]:
                del DecreaseTower.dot_stacks[enemy]
                del DecreaseTower.dot_start_time[enemy]
                del DecreaseTower.dot_end_time[enemy]
                del DecreaseTower.dot_cooldown[enemy]
                continue

            if now >= DecreaseTower.dot_cooldown[enemy]:
                dmg = DecreaseTower.dot_stacks[enemy] * self.damage
                enemy.health -= dmg
                self.total_damage += dmg

                DecreaseTower.dot_cooldown[enemy] = now + self.fire_rate

        DecreaseTower.did_tick_this_frame = True




