# student.py
import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from Level1Settings import *

class student(pygame.sprite.Sprite):
    def __init__(self, pos, game, lead, sprite, grid):
        super().__init__()
        self.grid = grid
        self.startPosition = pos
        self.game = game
        self.lead = lead  # Este é o sprite que este companion seguirá
        self.image = pygame.image.load(sprite)  # Adicione a imagem do seu companion
        self.rect = self.image.get_rect(center=pos)
        self.speed = 100  # velocidade de movimento em milissegundos
        self.path = []
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if (not self.path or now - self.last_update > self.speed) and self.lead.path:
            grid_data = [[0 if cell == 'x' or cell == 'H' else 1 for cell in row] for row in self.grid]
            grid = Grid(matrix=grid_data)
            start = grid.node(self.rect.x // TILESIZE, self.rect.y // TILESIZE)
            end = grid.node(self.lead.path[0][0], self.lead.path[0][1])  # Vá para o próximo ponto no caminho do líder
            finder = AStarFinder()
            path, runs = finder.find_path(start, end, grid)

            if path:
                self.path = path[1:]

        if self.path and now - self.last_update > self.speed:
            next_pos = self.path[0]
            self.rect.topleft = (next_pos[0]*TILESIZE, next_pos[1]*TILESIZE)
            self.path = self.path[1:]
            self.last_update = now