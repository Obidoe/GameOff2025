import pygame


class Map:
    def __init__(self, grid, tile_size):
        self.grid = grid
        self.tile_size = tile_size
        self.rows = len(grid)
        self.cols = len(grid[0])

    # Draw map on screen
    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                color = (255, 255, 255) if val == -1 else (0, 255, 0)
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (50, 50, 50), rect, 1)

    # Check if path
    def walkable(self, x, y):
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.grid[y][x] == 0
        return false

    # Check if outside path
    def buildable(self, x, y):
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.grid[y][x] == -1
        return false

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
