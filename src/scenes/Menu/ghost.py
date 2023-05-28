import pygame
import time
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Ghost(pygame.sprite.Sprite):
    def __init__(self, pos, speed, spawn_point):
        super().__init__()
        self.image = pygame.image.load('ghost.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.damage = 50
        self.speed = 90
        self.spawn_point = spawn_point
        self.path = []
        self.last_hit_time = 0
        self.TILESIZE = 33
        self.current_patrol_point_index = 0
        self.start_pos = spawn_point
        self.damage_timer = 0
        self.respawn_timer = 150
        self.last_update = pygame.time.get_ticks()

    def move_to(self, pos, grid):
        TILESIZE = self.TILESIZE
        start = grid.node(self.rect.x // TILESIZE, self.rect.y // TILESIZE)
        end = grid.node(pos[0] // TILESIZE, pos[1]// TILESIZE)
        finder = AStarFinder()
        path, runs = finder.find_path(start, end, grid)

        if path:
            self.path = path[1:]

        if not self.path:  # Verifica se o caminho anterior foi concluído
            if path:
                self.path = path[1:]
        
    def respawn(self):
        self.rect.topleft = self.spawn_point  # respawn ghost at the spawn point
        self.path = []
        self.damage_timer = 0
        self.respawn_timer = 300

    def is_near_player(self, player):
        return abs(self.rect.x - player.rect.x) < 50 and abs(self.rect.y - player.rect.y) < 50


    def handle_collision_with_player(self, player):
        if self.rect.colliderect(player.rect):
            if self.damage_timer <= 0:
                player.take_damage(self.damage)
                self.damage_timer = 180  # 3 seconds at 60 frames per second
                self.respawn_timer = 180  # 3 seconds at 60 frames per second
                self.kill()  # remove the ghost from all sprite groups
                return True
        return False

        

    def update(self):
        now = pygame.time.get_ticks()
        if self.path and now - self.last_update > self.speed:
            next_pos = self.path[0]
            self.rect.topleft = (next_pos[0]*self.TILESIZE, next_pos[1]*self.TILESIZE)
            self.path = self.path[1:]
            self.last_update = now
        if self.damage_timer > 0:
            self.damage_timer -= 1
        if self.respawn_timer > 0:
            self.respawn_timer -= 1