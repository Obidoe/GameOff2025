import pygame


class Map:
    def __init__(self, grid, tile_size):
        self.grid = grid
        self.tile_size = tile_size
        self.rows = len(grid)
        self.cols = len(grid[0])

    # Draw map
    def draw(self, screen):

        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                color = (20, 20, 30) if val == -1 else (0, 80, 80)  # darker path base
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size,
                                   self.tile_size, self.tile_size)
                pygame.draw.rect(screen, color, rect)

                if val == -1:
                    pygame.draw.rect(screen, (50, 50, 50), rect, 1)

        first_left_path = None
        for yy, row in enumerate(self.grid):
            for xx, v in enumerate(row):
                if v == 0:
                    if first_left_path is None or xx < first_left_path[0]:
                        first_left_path = (xx, yy)

        # Neon outline color
        glow_color = (0, 255, 255)

        # Draw neon outline
        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):

                if val != 0:
                    continue

                px = x * self.tile_size
                py = y * self.tile_size
                ts = self.tile_size

                # Top line
                if y == 0 or self.grid[y - 1][x] != 0:
                    pygame.draw.line(screen, glow_color, (px, py), (px + ts, py), 3)

                # Bottom line
                if y == self.rows - 1 or self.grid[y + 1][x] != 0:
                    pygame.draw.line(screen, glow_color, (px, py + ts), (px + ts, py + ts), 3)

                # Left line
                if (x, y) != first_left_path:
                    if x == 0 or self.grid[y][x - 1] != 0:
                        pygame.draw.line(screen, glow_color, (px, py), (px, py + ts), 3)

                # Right line
                if x == self.cols - 1 or self.grid[y][x + 1] != 0:
                    pygame.draw.line(screen, glow_color, (px + ts, py), (px + ts, py + ts), 3)

    # Check if path
    def walkable(self, x, y):
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.grid[y][x] == 0
        return False

    # Check if outside path
    def buildable(self, x, y):
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.grid[y][x] == -1
        return False

    # Convert pixel to tile
    def pix_to_tile(self, pos):
        px, py = pos
        return px // self.tile_size, py // self.tile_size

    # Convert tile to pixel
    def tile_to_pix_center(self, tile):
        tx, ty = tile
        resultx = ty * self.tile_size + self.tile_size // 2
        resulty = tx * self.tile_size + self.tile_size // 2
        return resultx, resulty

    # Check if tower is being placed on path or outside path
    def place_tower(self, mouse_pos, tower_group, ignore_tower=None):
        tile_x, tile_y = self.pix_to_tile(mouse_pos)

        if not self.buildable(tile_x, tile_y):
            return False

        for tower in tower_group:
            if tower is ignore_tower:
                continue
            if tower.rect.collidepoint(mouse_pos):
                return False

        return True


