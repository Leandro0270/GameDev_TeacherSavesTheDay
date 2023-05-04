import pygame
import time
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid

class ghost:
    def __init__(self, x, y, speed, damage, image, patrol_radius):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.patrol_radius = patrol_radius
        self.patrol_position = 0
        self.chase_start_time = 0
        self.chase_duration = 20

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.topleft = (self.x, self.y)

    def patrol(self):
        angle = 2 * pygame.math.pi * self.patrol_position / 360
        dx = int(self.patrol_radius * pygame.math.cos(angle))
        dy = int(self.patrol_radius * pygame.math.sin(angle))

        self.move(dx, dy)
        self.patrol_position = (self.patrol_position + 1) % 360

    def in_sight(self, player, sight_range):
        distance = ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5
        return distance <= sight_range

    def pathfinding(self, start, end, grid_data):
        grid = Grid(matrix=grid_data)
        start = grid.node(start[0], start[1])
        end = grid.node(end[0], end[1])

        finder = AStarFinder()
        path, _ = finder.find_path(start, end, grid)

        return path

    def chase(self, player, grid_data):
        path = self.pathfinding((self.x, self.y), (player.x, player.y), grid_data)
        if len(path) > 1:
            next_node = path[1]
            dx = next_node[0] - self.x
            dy = next_node[1] - self.y
            self.move(dx, dy)

    def collide_with_player(self, player):
        return self.rect.colliderect(player.rect)

    def update(self, player, grid_data, sight_range):
        if self.in_sight(player, sight_range):
            if self.chase_start_time == 0:
                self.chase_start_time = time.time()

            self.chase(player, grid_data)

            if self.collide_with_player(player):
                player.health -= self.damage

            if time.time() - self.chase_start_time > self.chase_duration:
                self.chase_start_time = 0
        else:
            if self.chase_start_time != 0:
                self.chase_start_time = 0

            self.patrol()

    def draw(self, screen):
        screen.blit(self.image, self.