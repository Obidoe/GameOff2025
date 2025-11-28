import pygame

class Slider:
    def __init__(self, x, y, width, height, initial_value=0.5):
        self.rect = pygame.Rect(x, y, width, height)
        self.knob_width = 20
        self.knob_rect = pygame.Rect(
            x + int(initial_value * (width - self.knob_width)),
            y - 5,
            self.knob_width,
            height + 10
        )
        self.dragging = False
        self.value = initial_value  # 0.0 to 1.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(event.pos):
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Move knob
                new_x = min(max(event.pos[0], self.rect.x), self.rect.x + self.rect.width - self.knob_width)
                self.knob_rect.x = new_x

                # Calculate new value
                self.value = (self.knob_rect.x - self.rect.x) / (self.rect.width - self.knob_width)

    def draw(self, screen):
        # Bar
        pygame.draw.rect(screen, (180, 180, 180), self.rect, border_radius=5)

        # Filled portion
        fill_rect = pygame.Rect(self.rect.x, self.rect.y,
                                (self.knob_rect.centerx - self.rect.x),
                                self.rect.height)
        pygame.draw.rect(screen, (28, 82, 38), fill_rect, border_radius=5)
        pygame.draw.rect(screen, (0, 255, 159), fill_rect, border_radius=5, width=2)

        # Knob
        pygame.draw.rect(screen, (255, 255, 255), self.knob_rect, border_radius=5)
