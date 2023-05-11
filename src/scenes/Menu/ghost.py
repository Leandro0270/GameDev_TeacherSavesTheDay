import pygame
import time
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid

class ghost:
    def __init__(self, x, y, speed, damage, image, patrol_distance, patrol_direction, player):
            self.x = x
            self.y = y
            self.speed = speed
            self.damage = damage
            self.image = pygame.image.load(image)
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.x, self.y)
            self.patrol_distance = patrol_distance
            self.patrol_direction = patrol_direction
            self.patrol_position = 0
            self.patrol_reversed = False
            self.chase_start_time = 0
            self.chase_duration = 20
            self.player = player

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.topleft = (self.x, self.y)


    def patrol(self):
        if self.patrol_position == self.patrol_distance:
            self.patrol_reversed = not self.patrol_reversed
            self.patrol_position = 0

        if self.patrol_direction == 'vertical':
            dy = -1 if self.patrol_reversed else 1
            self.move(0, dy)
        else: # horizontal
            dx = -1 if self.patrol_reversed else 1
            self.move(dx, 0)

        self.patrol_position += 1

    def in_sight(self, sight_range):
        distance = ((self.x - self.player.x) ** 2 + (self.y - self.player.y) ** 2) ** 0.5
        return distance <= sight_range

    def pathfinding(self, start, end, grid_data):
        grid = Grid(matrix=grid_data)
        start = grid.node(start[0], start[1])
        end = grid.node(end[0], end[1])

        finder = AStarFinder()
        path, _ = finder.find_path(start, end, grid)

        return path

    def chase(self, grid_data):
        path = self.pathfinding((self.x, self.y), (self.player.x, self.player.y), grid_data)
        if len(path) > 1:
            next_node = path[1]
            dx = next_node[0] - self.x
            dy = next_node[1] - self.y
            self.move(dx, dy)

    def collide_with_player(self, player):
        return self.rect.colliderect(player.rect)

    def update(self, player, grid_data, sight_range):
        if self.in_sight(sight_range):
            if self.chase_start_time == 0:
                self.chase_start_time = time.time()

            self.chase(grid_data)

            if self.collide_with_player(player):
                player.scarePlayer()
            if time.time() - self.chase_start_time > self.chase_duration:
                self.chase_start_time = 0
        else:
            if self.chase_start_time != 0:
                self.chase_start_time = 0

            self.patrol()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)