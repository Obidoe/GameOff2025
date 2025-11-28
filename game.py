import pygame
import random
import math
import numpy as np
from enemy.enemy import Enemy
from enemy.enemy2 import Enemy2
from enemy.enemy3 import Enemy3
from tower.tower import Tower
from tower.brute_force_tower import BruteForce
from tower.greedy_tower import GreedyTower
from tower.decrease_and_conquer_tower import DecreaseTower
from tower.transform_and_conquer_tower import TransformTower
from tower.divide_and_conquer_tower import DivideTower
from map import Map
from menu import Menu
from button import Button
from slider import Slider


class Gameloop:
    def __init__(self):
        # pygame setup
        pygame.init()

        pygame.mixer.init()
        pygame.mixer.music.load('cyberpunkmix4.ogg')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        self.clock = pygame.time.Clock()
        self.current_time = 0
        self.game_time = 0

        self.delta_time = 0.1
        self.screen_width = 1580
        self.screen_height = 720
        self.fps = 60

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),
                                              pygame.RESIZABLE | pygame.SCALED)
        pygame.display.set_caption("Algorithm Tower Defense")

        self.music_slider = Slider(self.screen_width // 2 - 150, self.screen_height * 1/6 + 220, 300, 10, initial_value=0.1)
        self.sound_slider = Slider(self.screen_width // 2 - 150, self.screen_height * 1/6 + 340, 300, 10, initial_value=0.1)

        # pause after wave
        self.game_pause = True
        # pause when press 'esc'
        self.esc_pause = False
        # start game display
        self.start_screen = True
        # tutorial
        self.how_to_play_screen = False
        self.tutorial_counter = 0
        # credits
        self.credits_screen = False

        # Side Panel Menu
        self.menu = Menu(self)

        # Player
        self.lives = 100
        self.gold = 200

        # Tower Management
        self.selected_tower = None

        # Waves
        self.waves = {
            1: [5, 0, 0],
            2: [10, 5, 0],
            3: [20, 8, 1],
            4: [20, 12, 5],
            5: [20, 20, 10]
        }

        self.clear_gold = [100, 200, 300, 400, 500]
        self.current_wave = 0
        self.wave_delay = 5000
        self.wave_cleared_time = None
        self.wave_waiting = False
        self.game_over = False

        self.spawn_interval = 100
        self.last_enemy_spawn = 0
        self.enemies_left_to_spawn = 0
        self.enemies_to_spawn_random = 0
        self.enemies_to_spawn_bfs = 0
        self.enemies_to_spawn_astar = 0

        self.big_font = pygame.font.SysFont("Arial", 144)
        self.medium_font = pygame.font.SysFont("Arial", 77)
        self.small_font = pygame.font.SysFont("Arial", 36)
        self.very_small_font = pygame.font.SysFont("Arial", 12)
        self.auto_size = max(12, int(self.screen_width * 0.02))
        self.auto_font = pygame.font.SysFont("Arial", self.auto_size)

        # images
        self.map_png = pygame.image.load('images/map.png').convert()

        self.pause_button_image = pygame.image.load('images/pause_button.png').convert()

        # init map
        self.tile_size = 64
        grid = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, 0, 0, 0, 0, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 0, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 0, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        ])
        self.map = Map(grid, self.tile_size)

        # Sprite groups
        self.enemy_group = pygame.sprite.Group()
        self.tower_group = pygame.sprite.Group()

        self.running = True

    def reset(self):
        self.current_time = 0
        self.game_time = 0
        self.lives = 100
        self.gold = 200
        self.selected_tower = None
        self.current_wave = 0
        self.wave_delay = 5000
        self.wave_cleared_time = None
        self.wave_waiting = False
        self.game_over = False
        self.last_enemy_spawn = 0
        self.enemies_left_to_spawn = 0
        self.enemies_to_spawn_random = 0
        self.enemies_to_spawn_bfs = 0
        self.enemies_to_spawn_astar = 0
        self.enemy_group = pygame.sprite.Group()
        self.tower_group = pygame.sprite.Group()

    def toggle_game_pause(self):
        self.game_pause = not self.game_pause

    def spawn_wave(self):
        self.current_wave += 1

        if self.current_wave not in self.waves:
            # win
            self.game_over = True
            return

        randoms, bfs, astar = self.waves[self.current_wave]
        print(f'Spawning wave {self.current_wave}: {randoms} random pathing enemies, {bfs} BFS enemies and '
              f'{astar} A* enemies!')

        self.enemies_to_spawn_random = randoms
        self.enemies_to_spawn_bfs = bfs
        self.enemies_to_spawn_astar = astar
        self.enemies_left_to_spawn = randoms + bfs + astar

        self.last_enemy_spawn = pygame.time.get_ticks()

    def create_tower(self, mouse_pos, tower_type):

        if self.selected_tower and self.selected_tower.placing:
            self.delete_tower()

        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()

        tower = tower_type(mouse_pos)
        if self.gold >= tower.cost:
            tower.placing = True
            self.selected_tower = tower
            self.menu.set_selected_tower(tower)
            self.tower_group.add(tower)
            tower.just_bought = True

    def select_tower(self, mouse_pos):
        for tower in self.tower_group:
            if tower.rect.collidepoint(mouse_pos):
                self.selected_tower = tower
                self.menu.set_selected_tower(tower)
                break
            else:
                self.selected_tower = None
                self.menu.set_selected_tower(None)

    def delete_tower(self):
        self.tower_group.remove(self.selected_tower)
        if not self.selected_tower.just_bought:
            self.gold += self.selected_tower.cost
        self.selected_tower = None

    def draw_menu_text(self, text, font, center, normal_color, hover_color, outline_color, mouse_pos):

        temp_surface = font.render(text, True, normal_color)
        rect = temp_surface.get_rect(center=center)

        hovered = rect.collidepoint(mouse_pos)
        color = hover_color if hovered else normal_color

        # Draw outline if hovered
        if hovered:
            for x, y in [
                (-3, 0), (3, 0), (0, -3), (0, 3),
                (-3, -3), (-3, 3), (3, -3), (3, 3)
            ]:
                outline_surface = font.render(text, True, outline_color)
                outline_rect = outline_surface.get_rect(center=(rect.centerx + x, rect.centery + y))
                self.screen.blit(outline_surface, outline_rect)

        # Draw main text
        surface = font.render(text, True, color)
        self.screen.blit(surface, rect)

        return rect

    def event_handler(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if self.start_screen:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    # play
                    if self.play_rect.collidepoint(mouse_pos):
                        self.start_screen = False
                        self.game_pause = True
                        self.spawn_wave()

                    # how to play
                    elif self.how_to_play_rect.collidepoint(mouse_pos):
                        self.start_screen = False
                        self.how_to_play_screen = True

                    # credits
                    elif self.credits_rect.collidepoint(mouse_pos):
                        self.start_screen = False
                        self.credits_screen = True

                continue

            if self.how_to_play_screen:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.tutorial_counter += 1

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.how_to_play_screen = False
                    self.start_screen = True
                continue
            if self.credits_screen:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.credits_screen = False
                    self.start_screen = True
                continue

            if self.esc_pause:

                self.music_slider.handle_event(event)
                self.sound_slider.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.resume_rect.collidepoint(mouse_pos):
                        self.esc_pause = False

                    # NEED TO MAKE THIS ACTUALLY RESET THE GAME
                    elif self.quit_rect.collidepoint(mouse_pos):
                        self.reset()
                        self.esc_pause = False
                        self.start_screen = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.esc_pause = not self.esc_pause

                if event.key == pygame.K_F10:
                    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),
                                                          pygame.FULLSCREEN | pygame.SCALED)

                if event.key == pygame.K_p:
                    self.game_pause = False

            if not self.esc_pause and not self.game_over:
                mouse_pos = pygame.mouse.get_pos()

                self.menu.handle_event(event)
                if self.menu.event_consumed:
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_pos[0] < self.screen_width and mouse_pos[1] < self.screen_height:

                        if event.button == 1:
                            print(self.selected_tower)

                            if self.selected_tower and self.selected_tower.placing:
                                tower = self.selected_tower
                                mouse_pos = pygame.mouse.get_pos()

                                if tower.__class__.__name__ == 'DecreaseTower':
                                    tower.locked = False

                                if self.map.place_tower(mouse_pos, self.tower_group, ignore_tower=tower):
                                    tower.placing = False
                                    tower.rect.center = mouse_pos

                                    if getattr(tower, 'just_bought', False):
                                        self.gold -= tower.cost
                                        tower.just_bought = False
                                return

                            if self.selected_tower.__class__.__name__ == 'DecreaseTower' \
                                    and not self.selected_tower.locked:
                                self.selected_tower.get_click(mouse_pos)
                                self.selected_tower.locked = True

                            self.select_tower(mouse_pos)

    def update_running(self):
        # Update side panel
        self.menu.update(pygame.mouse.get_pos())

        # Update Groups
        self.enemy_group.update()
        DecreaseTower.did_tick_this_frame = False
        self.tower_group.update(self.enemy_group, self.current_time)

        # Spawn Waves
        if self.enemies_left_to_spawn > 0:
            now = pygame.time.get_ticks()

            if now - self.last_enemy_spawn >= self.spawn_interval:
                self.last_enemy_spawn = now
                self.enemies_left_to_spawn -= 1

                if self.enemies_to_spawn_random > 0:
                    enemy = Enemy(self.map, self, start_tile=(0, 0))
                    self.enemy_group.add(enemy)
                    self.enemies_to_spawn_random -= 1

                elif self.enemies_to_spawn_bfs > 0:
                    enemy = Enemy2(self.map, self, start_tile=(0, 0))
                    self.enemy_group.add(enemy)
                    self.enemies_to_spawn_bfs -= 1

                elif self.enemies_to_spawn_astar > 0:
                    enemy = Enemy3(self.map, self, start_tile=(0, 0))
                    self.enemy_group.add(enemy)
                    self.enemies_to_spawn_astar -= 1

        # check if wave complete
        if (self.enemies_left_to_spawn == 0
                and len(self.enemy_group) == 0
                and not self.wave_waiting):
            if self.current_wave in self.waves:
                self.gold += self.clear_gold[self.current_wave - 1]
            self.wave_waiting = True
            self.wave_cleared_time = pygame.time.get_ticks()

        # wait then start next wave
        if self.wave_waiting:
            now = pygame.time.get_ticks()
            if not self.game_over:
                wave_clear_text = self.big_font.render(f'Wave {self.current_wave} 'f'cleared!', True,
                                                       'WHITE')
                wave_clear_rect = wave_clear_text.get_rect(center=(self.screen_width / 2 - 150, self.screen_height / 2))
                self.screen.blit(wave_clear_text, wave_clear_rect)
            if now - self.wave_cleared_time >= self.wave_delay:
                self.wave_waiting = False
                self.game_pause = True
                self.spawn_wave()

        # check if player has any lives left
        if self.lives <= 0:
            self.game_over = True

        # if player wins
        if self.lives > 0 and self.game_over:
            game_over_text = self.big_font.render(f'YOU WIN', True, 'WHITE')
            game_over_text_rect = game_over_text.get_rect(center=(self.screen_width / 2 - 150, self.screen_height / 2))
            self.screen.blit(game_over_text, game_over_text_rect)

    def run(self):

        while self.running:

            # frame rate timing
            self.delta_time = self.clock.tick(self.fps) / 1000
            self.delta_time = max(0.001, min(0.1, self.delta_time))

            # start screen
            if self.start_screen:
                self.screen.fill((20, 20, 30))

                text_color = (255, 255, 255)
                hover_color = (90, 0, 120)
                outline_color = (189, 0, 255)

                # title
                title_text = 'ALGORITHM TD'
                title_pos = (self.screen_width // 2, self.screen_height // 2 - 250)
                for x, y in [(-3, 0), (3, 0), (0, -3), (0, 3), (-3, -3), (-3, 3), (3, -3), (3, 3)]:
                    outline = self.big_font.render(title_text, True, (0, 255, 255))
                    self.screen.blit(outline, outline.get_rect(center=(title_pos[0] + x, title_pos[1] + y)))

                title = self.big_font.render(title_text, True, (0, 80, 80))
                self.screen.blit(title, title.get_rect(center=title_pos))

                mouse_pos = pygame.mouse.get_pos()

                self.play_rect = self.draw_menu_text(
                    "PLAY",
                    self.medium_font,
                    (self.screen_width // 2, self.screen_height // 2 - 50),
                    text_color,
                    hover_color,
                    outline_color,
                    mouse_pos
                )

                self.how_to_play_rect = self.draw_menu_text(
                    "HOW TO PLAY",
                    self.medium_font,
                    (self.screen_width // 2, self.screen_height // 2 + 100),
                    text_color,
                    hover_color,
                    outline_color,
                    mouse_pos
                )

                self.credits_rect = self.draw_menu_text(
                    "CREDITS",
                    self.medium_font,
                    (self.screen_width // 2, self.screen_height // 2 + 250),
                    text_color,
                    hover_color,
                    outline_color,
                    mouse_pos
                )

                self.event_handler()
                pygame.display.flip()
                continue

            if self.how_to_play_screen:
                self.screen.fill((20, 20, 30))
                self.map.draw(self.screen)
                self.menu.draw(self.screen)
                background = pygame.Surface((self.screen_width * 2/3, self.screen_height * 2/3), pygame.SRCALPHA)
                background_rect = background.get_rect(center=(self.screen_width // 2 - 150, self.screen_height // 2))
                background.fill((20, 20, 30, 220))

                self.screen.blit(background, background_rect)
                pygame.draw.rect(self.screen, (189, 0, 255), background_rect, width=2, border_radius=10)

                t0 = 'Welcome to Algorithm TD!'
                t1 = 'Your goal in Algorithm TD is to defend against the hostile viruses trying to infiltrate your system!'
                t2 = 'The enemy viruses spawn in the top left corner and they enter your system if they reach the bottom right corner'
                # Visualize this with thick red rect ^
                t3 = 'You must utilize towers that have specially crafted algorithms to detect and destroy viruses.'
                t4 = 'You can purchase these towers from the menu on the right side of the screen.'
                # Visualize this with thick red rect ^
                t5 = 'Once you have purchased a tower, you can place it anywhere within the dark grid on the map.'
                t6 = 'You cannot place towers directly onto the pathway the viruses use.'
                t7 = 'After you have strategically placed your defenses, click the "Play" button at the bottom of the side menu. '
                t8 = 'The temporary barrier keeping the viruses out of your system will be disabled.'
                t9 = 'When the wave of viruses have either been defeated or reached your system, a new temporary barrier will be setup. '
                t10 = 'This will give you time to prepare for the next wave. '
                t11 = 'When you are ready, be sure to click the "Play" button to start the next wave'
                t12 = 'If you can successfully defend your system against 15 waves of virus attacks, you will be victorious! '
                t13 = 'If you run out of lives, however... the viruses will take over your system and shut you down.'
                t14 = 'Enjoy!'
                text_list = []
                offset = 0
                font = pygame.font.SysFont("Arial", 19)

                if self.tutorial_counter == 0:
                    text_list = [t0, t1, t2]
                    pygame.draw.rect(self.screen, (255, 0, 0), (0, 0, 64, 66), width=6)
                    pygame.draw.rect(self.screen, (0, 255, 0), (19*64, 10*64, 65, 68), width=6)
                if self.tutorial_counter == 1:
                    text_list = [t0, t1, t2, t3, t4, t5, t6]
                    pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_width - 300, 0, 300,
                                                                self.screen_height), width=6)
                if self.tutorial_counter == 2:
                    text_list = [t7, t8, t9, t10, t11, t12, t13, t14]
                    pygame.draw.rect(self.screen, (255, 0, 0), (self.screen_width - 290, self.screen_height - 70, 280, 60), width=6)
                if self.tutorial_counter >= 3:
                    self.how_to_play_screen = False
                    self.start_screen = True
                    self.tutorial_counter = 0

                for t in text_list:
                    text = font.render(t, True, 'WHITE')
                    text_rect = text.get_rect(center=(background_rect.centerx, background_rect.centery - 200 + offset))
                    self.screen.blit(text, text_rect)
                    offset += 55

                #return_text = self.small_font.render(f'Click anywhere to return', True, 'WHITE')
                #return_text_rect = return_text.get_rect(center=(self.screen_width // 2, self.screen_height - 25))
                #self.screen.blit(return_text, return_text_rect)
                self.event_handler()
                pygame.display.flip()
                continue

            if self.credits_screen:
                self.screen.fill((20, 20, 30))
                credit_dict = {
                    'Zac Adams (Obidoe)': 'Developer',
                    'Harry Rai (OffensiveChip)': 'Developer',
                    'Jasraj Gosal (JazzUni)': 'Developer | 2D Artist'
                }
                offset = 0
                for name in credit_dict.keys():
                    credit_text = self.small_font.render(f'{name}: {credit_dict[name]}', True, 'WHITE')
                    credit_text_rect = credit_text.get_rect(center=(self.screen_width // 2,
                                                                    self.screen_height // 2 - 200 + offset))
                    self.screen.blit(credit_text, credit_text_rect)
                    offset += 100

                return_text = self.small_font.render(f'Click anywhere to return', True, 'WHITE')
                return_text_rect = return_text.get_rect(center=(self.screen_width // 2, self.screen_height - 25))
                self.screen.blit(return_text, return_text_rect)

                self.event_handler()
                pygame.display.flip()
                continue

            # draw map
            self.map.draw(self.screen)

            # draw transform blast zones UNDER everything else
            for tower in self.tower_group:
                if tower.placing:
                    tower.rect.center = pygame.mouse.get_pos()
                if isinstance(tower, TransformTower):
                    tower.draw_blast_zone(self.screen, self.current_time)

            # event handler
            self.event_handler()

            # Draw Groups
            for enemy in self.enemy_group:
                enemy.draw(self.screen)
            for tower in self.tower_group:
                tower.draw(self.screen, self.current_time)

            # Draw Selected
            if self.selected_tower:
                t = self.selected_tower
                pygame.draw.rect(self.screen, (255, 0, 0),
                                 (t.rect.x - 5, t.rect.y - 5, t.rect.width + 10, t.rect.height + 10), width=2)

                # draw radius
                color = (255, 0, 0, 160)
                transparent_surface = pygame.Surface((t.range * 2, t.range * 2), pygame.SRCALPHA)
                pygame.draw.circle(transparent_surface, color, (t.range, t.range), t.range, width=2)
                self.screen.blit(transparent_surface, (t.rect.centerx - t.range, t.rect.centery - t.range))

            self.menu.update(pygame.mouse.get_pos())
            self.menu.draw(self.screen)

            # Game paused via esc
            if self.esc_pause:

                text_color = (255, 255, 255)
                hover_color = (28, 82, 38)
                outline_color = (0, 255, 159)

                darken_surface = pygame.Surface((self.screen_width, self.screen_height))
                darken_surface.fill((0, 0, 0))
                darken_surface.set_alpha(155)
                self.screen.blit(darken_surface, (0, 0))

                pause_menu = pygame.Surface((self.screen_width * 2/3, self.screen_height * 2/3))
                pause_menu_rect = pause_menu.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
                pause_menu.fill((20, 20, 30))

                self.screen.blit(pause_menu, pause_menu_rect)
                pygame.draw.rect(self.screen, (0, 255, 159), pause_menu_rect, width=2, border_radius=10)

                mouse_pos = pygame.mouse.get_pos()

                self.resume_rect = self.draw_menu_text(
                    "RESUME",
                    self.medium_font,
                    (pause_menu_rect.centerx, pause_menu_rect.y + 60),
                    text_color,
                    hover_color,
                    outline_color,
                    mouse_pos
                )
                self.quit_rect = self.draw_menu_text(
                    "QUIT TO MAIN MENU",
                    self.medium_font,
                    (pause_menu_rect.centerx, pause_menu_rect.y + 420),
                    text_color,
                    hover_color,
                    outline_color,
                    mouse_pos
                )

                music_vol = self.medium_font.render(f'MUSIC VOLUME', True, 'WHITE')
                music_vol_rect = music_vol.get_rect(center=(pause_menu_rect.centerx,
                                                                              pause_menu_rect.y + 170))
                self.screen.blit(music_vol, music_vol_rect)
                self.music_slider.draw(self.screen)
                self.sound_slider.draw(self.screen)

                sfx_vol = self.medium_font.render(f'SFX VOLUME', True, 'WHITE')
                sfx_vol_rect = sfx_vol.get_rect(center=(pause_menu_rect.centerx,
                                                                              pause_menu_rect.y + 290))
                self.screen.blit(sfx_vol, sfx_vol_rect)

                # Update music
                pygame.mixer.music.set_volume(self.music_slider.value)

                pygame.display.flip()
                continue

            # Game paused after wave
            if self.game_pause and not self.game_over:
                pygame.display.flip()
                continue

            # Game over!
            if self.game_over and self.lives <= 0:
                game_over_text = self.big_font.render(f'GAME OVER', True, 'WHITE')
                game_over_text_rect = game_over_text.get_rect(center=(self.screen_width / 2 - 150,
                                                                      self.screen_height / 2))
                self.screen.blit(game_over_text, game_over_text_rect)
                pygame.display.flip()
                continue

            # Game not paused
            else:
                self.update_running()
                self.current_time += self.delta_time

            pygame.display.flip()

        pygame.quit()
