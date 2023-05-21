from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import pygame

class Ghost(pygame.sprite.Sprite):
    def __init__(self, pos, sprite, speed, grid, tileSize, player):
        super().__init__()
        self.player = player
        self.image = pygame.image.load(sprite)
        self.rect = self.image.get_rect(center=pos)
        self.start_pos = pos
        self.speed = speed
        self.path = []
        self.grid = grid
        self.tileSize = tileSize
        self.patrol_points = self.get_patrol_points()
        self.last_update = pygame.time.get_ticks()

    def get_patrol_points(self):
        patrol_points = []
        print(self.grid)
        for row_index, row in enumerate(self.grid):
            for col_index, col in enumerate(row):
                if col == 'ep':
                    patrol_points.append((col_index, row_index))
        print(patrol_points)
        return patrol_points

    def update(self):
        now = pygame.time.get_ticks()
        if not self.path or now - self.last_update > self.speed * 1000:
            self.path = self.calculate_path()
            self.last_update = now
        if self.path and now - self.last_update > self.speed * 10:
            next_pos = self.path[0]
            self.rect.topleft = (next_pos[0] * self.tileSize, next_pos[1] * self.tileSize)
            self.path = self.path[1:]
            self.last_update = now

    def calculate_path(self):
        grid_data = [[1 if cell == 'x' else 0 for cell in row] for row in self.grid]
        grid = Grid(matrix=grid_data)
        path = []
        start = grid.node(self.rect.x // self.tileSize, self.rect.y // self.tileSize)
        for patrol_point in self.patrol_points:
            end = grid.node(patrol_point[0], patrol_point[1])
            finder = AStarFinder()
            patrol_path, _ = finder.find_path(start, end, grid)
            path.extend(patrol_path[1:])  # Exclude the starting point for all paths except the first
            start = end
        return path

    def reset_position(self):
        self.rect.topleft = self.start_pos