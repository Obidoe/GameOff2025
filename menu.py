import pygame
from button import Button
from tower.tower import Tower
from tower.brute_force_tower import BruteForce
from tower.greedy_tower import GreedyTower
from tower.decrease_and_conquer_tower import DecreaseTower
from tower.transform_and_conquer_tower import TransformTower
from tower.divide_and_conquer_tower import DivideTower


class Menu:
    def __init__(self, game, width=300):
        self.game = game
        self.width = width
        self.font = pygame.font.Font(None, 22)
        self.title_font = pygame.font.Font(None, 36)
        self.event_consumed = False

        self.buttons = []
        self.selected_tower = None

        panel_x = self.game.screen_width - self.width

        # Game Buttons
        self.buttons.append(Button(
            (panel_x + 20, 660, 260, 40),
            lambda: 'Play' if self.game.game_pause else 'Pause',
            lambda: self.game.toggle_game_pause(),
            desc='Pause or resume gameplay'
        ))

        self.buttons.append(Button(
            (panel_x + 20, 610, 260, 40),
            'Move Tower',
            lambda: setattr(self.game.selected_tower, 'placing', True) if self.game.selected_tower else None,
            desc='Pick up selected tower'
        ))

        self.buttons.append(Button(
            (panel_x + 20, 560, 260, 40),
            'Delete Tower',
            lambda: self.game.delete_tower(),
            desc='Delete selected tower'
        ))

        # Tower Buttons
        panel_width = self.width
        padding_y = 20
        cols = 2

        # List of towers
        towers = [
            (Tower, 'MonoRay Pulse', 'Basic beam tower'),
            (BruteForce, 'Burst Compiler', 'Burst Compiler - Brute Force\n100G'),
            (GreedyTower, 'Greedcore Extractor', 'Greedy'),
            (DecreaseTower, 'Firewall EX', 'Decrease and Conquer'),
            (TransformTower, 'Quantum Dragfield', 'Transform and Conquer'),
            (DivideTower, 'ForkRay Matrix', 'Divide and Conquer')
        ]

        button_width = (panel_width - (cols + 1) * padding_y) // cols
        button_height = 50

        for index, (tower_class, label, desc) in enumerate(towers):
            col = index % cols
            row = index // cols

            x = panel_x + padding_y + col * (button_width + padding_y)
            y = padding_y + row * (button_height + padding_y) + 90

            self.buttons.append(
                Button((x, y, button_width, button_height), label,
                       lambda cls=tower_class: self.game.create_tower(None, cls),
                       desc=desc)
            )

    def update(self, mouse_pos):
        for b in self.buttons:
            b.update_hover(mouse_pos)

    def handle_event(self, event):
        self.event_consumed = False

        for b in self.buttons:
            if b.handle_event(event):
                self.event_consumed = True
                return

    def set_selected_tower(self, tower):
        self.selected_tower = tower

    def draw(self, screen):
        panel_x = self.game.screen_width - self.width

        # Back panel
        pygame.draw.rect(screen, (20, 20, 30), (panel_x, 0, self.width, self.game.screen_height))
        pygame.draw.rect(screen, (0, 240, 255), (panel_x, 0, self.width, self.game.screen_height), 1)

        # Display HP and Gold
        hp_text = self.title_font.render(f'Current Lives: {self.game.lives}', True, (220, 220, 255))
        hp_text_rect = hp_text.get_rect(center=(panel_x + self.width / 2, 30))
        screen.blit(hp_text, hp_text_rect)

        gold_text = self.title_font.render(f'Current Gold: {self.game.gold}', True, (220, 220, 255))
        gold_text_rect = gold_text.get_rect(center=(panel_x + self.width / 2, 60))
        screen.blit(gold_text, gold_text_rect)

        pygame.draw.line(screen, (0, 240, 255), (panel_x, 90), (panel_x + 300, 90))
        pygame.draw.line(screen, (0, 240, 255), (panel_x, 320), (panel_x + 300, 320))

        # Buttons
        draw_when_selected = ['Move Tower', 'Delete Tower']
        for b in self.buttons:
            if b.text in draw_when_selected and not self.game.selected_tower:
                continue
            b.draw(screen, self.font)

        # Tower info
        if self.selected_tower:
            # Selected tower info title
            t_info = self.title_font.render(f'Tower Information', True, (220, 220, 255))
            t_info_rect = t_info.get_rect(center=(panel_x + self.width / 2, 350))
            screen.blit(t_info, t_info_rect)

            tower = self.selected_tower
            x = panel_x + 20
            y = 375
            info = [
                f'Selected: {tower.display_name}',
                f'Damage: {tower.damage}',
                f'Range: {tower.range} units',
                f'Fire Rate: {round(tower.fire_rate, 2)} per second'
            ]
            if tower.display_name == 'GreedCore Extractor':
                info.append(f'Gold Earned: {tower.gold_earned}')

            for line in info:
                surf = self.font.render(line, True, (220, 220, 255))
                screen.blit(surf, (x, y))
                y += 28

        # Tooltip (pop out window)
        mouse_pos = pygame.mouse.get_pos()
        for b in self.buttons:
            if b.text in draw_when_selected and not self.game.selected_tower:
                continue
            if b.hover and b.description:
                text = b.description
                surf = self.font.render(text, True, (255, 255, 255))
                rect = surf.get_rect(topleft=(mouse_pos[0] + 12, mouse_pos[1] + 12))
                pygame.draw.rect(screen, (40, 40, 60), rect.inflate(10, 10), border_radius=4)
                screen.blit(surf, rect)

