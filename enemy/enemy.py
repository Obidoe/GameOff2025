import pygame
from pygame.math import Vector2


class Enemy(pygame.sprite.Sprite):
    def __init__(self, points, image):
        pygame.sprite.Sprite.__init__(self)
        self.points = points
        self.pos = Vector2(self.points[0])
        self.next_point = 1
        self.speed = 5
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.move()

    def move(self):
        if self.next_point < len(self.points):
            self.next = Vector2(self.points[self.next_point])
            self.movement = self.next - self.pos
        # Loop movement
        else:
            self.pos = Vector2(self.points[0])
            self.next_point = 0
            # self.kill()

        dist = self.movement.length()
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.next_point += 1

        self.rect.center = self.pos
