import pygame
from pygame.math import Vector2
from tower.tower import Tower, neon_outline


class DivideTower(Tower):
    cost = 250
    count = 0

    def __init__(self, pos):
        super().__init__(pos)
        raw = pygame.image.load('images/divide.png').convert_alpha()
        self.image = neon_outline(raw, color='WHITE', thickness=4)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.range = 300
        self.damage = 1
        self.fire_rate = 2
        self.cost = DivideTower.cost
        self.beams = []
        self.max_jumps = 2
        self.jump_radius = 100
        self.display_name = f'ForkRay Matrix{self.index}'
        self.attack_sound = pygame.mixer.Sound('sfx/laser13.wav')
        Tower.sound_manager.sfx_sounds.append(self.attack_sound)
        self.attack_sound.set_volume(Tower.sound_manager.sound_slider.value)

    def enemy_distance(self, enemy1, enemy2):
        return ((enemy1[0] - enemy2[0]) ** 2 + (enemy1[1] - enemy2[1]) ** 2) ** 0.5

    def shoot(self, target, current_time, enemies=None):
        self.attack_sound.play()
        self.last_shot_time = current_time

        hit_chain = []
        already_hit = set()

        current_set = [(target, self.rect.center)]

        # loops number of jumps
        # this whole section is basically like finding a tree of closest enemies
        # lightning branches / splits each jump
        for i in range(self.max_jumps + 1):
            next_set = []
            if not current_set:
                break

            for current_enemy, start_pos in current_set:

                hit_chain.append({
                    'start': start_pos,
                    'end': current_enemy.rect.center,
                    'time': current_time
                })

                current_enemy.health -= self.damage
                self.total_damage += self.damage
                already_hit.add(current_enemy)

                parent_pos = current_enemy.rect.center

                remaining = [
                    enemy for enemy in enemies
                    if enemy not in already_hit and
                       self.enemy_distance(enemy.rect.center, parent_pos) <= self.jump_radius
                ]

                remaining.sort(key=lambda e: Vector2(e.rect.center).distance_to(parent_pos))
                children = remaining[:2]

                for child in children:
                    next_set.append((child, parent_pos))

            if not next_set:
                break
            current_set = next_set

        self.beams.extend(hit_chain)

        print(f'Shooting at {target} dealing {self.damage} damage!')
        print(f'Total damage so far: {self.total_damage}')

    def draw(self, screen, current_time):
        # draw sprite
        screen.blit(self.image, self.rect)

        age = (current_time - self.last_shot_time) / self.shot_display_time
        alpha = int(255 * (1 - age))
        transparent_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        # draw beams
        for beam in self.beams[:]:
            if current_time - beam['time'] < self.shot_display_time:
                pygame.draw.line(transparent_surface, (255, 210, 0, alpha), beam['start'], beam['end'], 6)
                pygame.draw.line(transparent_surface, (255, 230, 0, alpha), beam['start'], beam['end'], 4)
                pygame.draw.line(transparent_surface, (255, 255, 0, alpha), beam['start'], beam['end'], 2)
                screen.blit(transparent_surface, (0, 0))
            else:
                self.beams.remove(beam)

    def update(self, enemies, current_time):
        if self.placing:
            return
        target = self.detect_enemy(enemies)
        if target and self.can_shoot(current_time):
            self.shoot(target, current_time, enemies)
