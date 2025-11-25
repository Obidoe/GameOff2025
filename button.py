import pygame


class Button:
    def __init__(self, rect, text, callback, desc=''):
        self.rect = pygame.Rect(rect)
        self._text = text
        self.callback = callback
        self.description = desc
        self.hover = False

    def draw(self, screen, font):
        # Background
        color = (20, 20, 30) if not self.hover else (100, 120, 150)
        pygame.draw.rect(screen, color, self.rect, border_radius=10)

        # Split into lines
        lines = self.text.split("\n")

        # Start with given font size and shrink until all lines fit width
        size = font.get_height()
        fitted_font = pygame.font.SysFont(None, size)

        max_width = int(self.rect.width * 0.99)

        # Shrink until widest line fits
        while True:
            rendered = [fitted_font.render(line, True, (220, 220, 255)) for line in lines]
            widest = max(surf.get_width() for surf in rendered)
            total_height = sum(surf.get_height() for surf in rendered)

            if widest <= max_width and total_height <= self.rect.height * 0.9:
                break

            size -= 1
            if size < 8:
                break
            fitted_font = pygame.font.SysFont(None, size)

        rendered = [fitted_font.render(line, True, (220, 220, 255)) for line in lines]

        # Center
        total_height = sum(surf.get_height() for surf in rendered)
        y = self.rect.centery - total_height // 2

        # Draw each line centered
        for surf in rendered:
            text_rect = surf.get_rect(center=(self.rect.centerx, y + surf.get_height() // 2))
            screen.blit(surf, text_rect)
            y += surf.get_height()

        # Border
        pygame.draw.rect(screen, (189, 0, 255), self.rect, width=2, border_radius=10)

    def update_hover(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
                return True
        return False

    @property
    def text(self):
        if callable(self._text):
            return self._text()
        return self._text
