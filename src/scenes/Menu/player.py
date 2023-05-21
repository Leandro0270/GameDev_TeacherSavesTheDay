# player.py
import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from Level1Settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.life =100
        self.image = pygame.image.load('player.png')  # Adicione a imagem do seu jogador
        self.rect = self.image.get_rect(center=pos)
        self.speed = 100  # velocidade de movimento em milissegundos
        self.path = []
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if self.path and now - self.last_update > self.speed:
            next_pos = self.path[0]
            self.rect.topleft = (next_pos[0]*TILESIZE, next_pos[1]*TILESIZE)
            self.path = self.path[1:]
            self.last_update = now

    def move_to(self, pos, grid):
        start = grid.node(self.rect.x // TILESIZE, self.rect.y // TILESIZE)
        end = grid.node(pos[0] // TILESIZE, pos[1] // TILESIZE)
        finder = AStarFinder()
        path, runs = finder.find_path(start, end, grid)

        if path:
            self.path = path[1:]

    def take_damage(self, damage):
        self.life   =- damage