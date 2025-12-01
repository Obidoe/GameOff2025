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
            desc='Pause or resume gameplay.'
        ))

        self.buttons.append(Button(
            (panel_x + 20, 610, 260, 40),
            'Move Tower',
            lambda: self.game.move_tower(),
            desc='Pick up selected tower.\nCost: 50 Gold'
        ))

        self.buttons.append(Button(
            (panel_x + 20, 560, 260, 40),
            'Delete Tower',
            lambda: self.game.delete_tower(),
            desc='Delete selected tower.\nReturns 50% of initial tower cost.'
        ))

        # Tower Buttons
        panel_width = self.width
        padding_y = 20
        cols = 2

        # List of towers
        towers = [
            (Tower, 'MonoRay Pulse', f'MonoRay Pulse\nCost: {Tower.cost} Gold\nA basic tower that shoots a beam at the closest enemy.'),
            (BruteForce, 'Burst Compiler', f'Burst Compiler\nCost: {BruteForce.cost} Gold\nA spreadshot tower that uses brute force to take down the closest enemy.'),
            (GreedyTower, 'Greedcore Extractor', f'Greedcore Extractor\nCost: {GreedyTower.cost} Gold\nA long-range tower that targets low health enemies and extracts extra gold on kill.'),
            (DecreaseTower, 'Firewall EX', f'Firewall EX\nCost: {DecreaseTower.cost} Gold\nThis tower allows for the placement of a firewall. Enemies that pass through the fire wall take damage over time.'),
            (TransformTower, 'Quantum Dragfield', f'Quantum Dragfield\nCost: {TransformTower.cost} Gold\nA short range tower that shoots a beam at the closest enemy which creates a blast zone and slows all enemies in the surrounding area.'),
            (DivideTower, 'ForkRay Matrix', f'ForkRay Matrix\nCost: {DivideTower.cost} Gold\nA tower that shoots a beam at the closest enemy which will jump to nearby enemies, creating a chain of beam attacks.')
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

            btn = Button((x, y, button_width, button_height), label,
                         lambda cls=tower_class: self.game.create_tower(None, cls),
                         desc=desc)
            btn.tower_class = tower_class  # store class for dynamic cost
            self.buttons.append(btn)

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

        hp_text = 'Current Lives: '
        lives_value = str(self.game.lives)

        if self.game.lives <= 25:
            hp_color = 'RED'
        elif self.game.lives <= 50:
            hp_color = 'YELLOW'
        else:
            hp_color = 'GREEN'

        hp_surface = self.title_font.render(hp_text, True, (220, 220, 255))
        value_surface = self.title_font.render(lives_value, True, hp_color)

        hp_text_rect = hp_surface.get_rect(center=(panel_x + self.width / 2 - 20, 30))
        value_rect = value_surface.get_rect(midleft=hp_text_rect.midright)

        screen.blit(hp_surface, hp_text_rect)
        screen.blit(value_surface, value_rect)

        gold_text = 'Current Gold: '
        gold_value = str(self.game.gold)

        gold_text = self.title_font.render(gold_text, True, (220, 220, 255))
        gold_value = self.title_font.render(gold_value, True, 'GOLD')

        gold_text_rect = gold_text.get_rect(center=(panel_x + self.width / 2 - 20, 60))
        gold_value_rect = gold_value.get_rect(midleft=gold_text_rect.midright)

        screen.blit(gold_text, gold_text_rect)
        screen.blit(gold_value, gold_value_rect)

        pygame.draw.line(screen, (0, 240, 255), (panel_x, 90), (panel_x + 300, 90))
        pygame.draw.line(screen, (0, 240, 255), (panel_x, 320), (panel_x + 300, 320))

        # Buttons
        draw_when_selected = ['Move Tower', 'Delete Tower']
        for b in self.buttons:
            if b.text in draw_when_selected and not self.game.selected_tower:
                continue
            b.draw(screen, self.font)

            if hasattr(b, 'tower_class'):
                cost_text = f'{b.tower_class.cost}G'
                cost_surf = self.font.render(cost_text, True, 'GOLD')
                cost_rect = cost_surf.get_rect(center=(b.rect.centerx, b.rect.bottom + 12))
                screen.blit(cost_surf, cost_rect)

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
                f'Fire Rate: {round(tower.fire_rate, 2)} per second',
                f'Total Damage Done: {tower.total_damage}'
            ]
            if tower.__class__.__name__ == 'GreedyTower':
                info.append(f'Gold Earned: {tower.gold_earned}')

            for line in info:
                surf = self.font.render(line, True, (220, 220, 255))
                screen.blit(surf, (x, y))
                y += 28

        # Draw tooltip
        mouse_pos = pygame.mouse.get_pos()
        for b in self.buttons:
            if b.text in draw_when_selected and not self.game.selected_tower:
                continue
            if b.hover and b.description:
                self.draw_tooltip(screen, b.description, mouse_pos)

    def draw_tooltip(self, screen, text, mouse_pos, max_width=300, padding=6, line_spacing=4):
        paragraphs = text.split('\n')
        lines = []

        for para in paragraphs:
            words = para.split(' ')
            current_line = ''
            for word in words:
                test_line = current_line + (' ' if current_line else '') + word
                test_surf = self.font.render(test_line, True, (255, 255, 255))
                if test_surf.get_width() > max_width - 2 * padding:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
                else:
                    current_line = test_line
            if current_line:
                lines.append(current_line)

        line_height = self.font.get_linesize()
        tooltip_height = line_height * len(lines) + line_spacing * (len(lines) - 1) + 2 * padding
        tooltip_width = min(max_width, max(
            self.font.render(line, True, (255, 255, 255)).get_width() for line in lines) + 2 * padding)

        rect = pygame.Rect(mouse_pos[0] + 12, mouse_pos[1] + 12, tooltip_width, tooltip_height)

        screen_width, screen_height = screen.get_size()
        if rect.right > screen_width:
            rect.right = screen_width - 5
        if rect.bottom > screen_height:
            rect.bottom = screen_height - 5
        if rect.left < 0:
            rect.left = 5
        if rect.top < 0:
            rect.top = 5

        pygame.draw.rect(screen, (20, 20, 30), rect, border_radius=4)
        pygame.draw.rect(screen, (189, 0, 255), rect, border_radius=4, width=2)

        y_offset = rect.top + padding
        for line in lines:
            surf = self.font.render(line, True, (255, 255, 255))
            x_offset = rect.left + (rect.width - surf.get_width()) // 2
            screen.blit(surf, (x_offset, y_offset))
            y_offset += line_height + line_spacing
