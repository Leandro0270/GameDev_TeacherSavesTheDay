import pygame
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid

class Teacher:
    def __init__(self, x, y, speed, health, image):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.inventory = []
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.topleft = (self.x, self.y)

    def add_item_to_inventory(self, item):
        self.inventory.append(item)

    def check_collision(self, obstacles):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle.rect):
                return True
        return False

    def pathfinding(self, start, end, grid_data):
        grid = Grid(matrix=grid_data)
        start = grid.node(start[0], start[1])
        end = grid.node(end[0], end[1])

        finder = AStarFinder()
        path, _ = finder.find_path(start, end, grid)

        return path

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)