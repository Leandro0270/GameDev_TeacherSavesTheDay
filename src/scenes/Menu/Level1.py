# Level1.py
import pygame
from Level1Settings import *
from tile import Tile
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from player import Player  # Importação da classe Player

class Level1:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        self.Level1_MOUSE_POS = pygame.mouse.get_pos()
        self.bg = pygame.image.load('level1BG.png').convert_alpha()
        self.generateMap()

    def generateMap(self):
        for row_index,row in enumerate(LEVEL1_GRIDMAP):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if(col == 'x'):
                    Tile((x,y),[self.visible_sprites,self.obstacles_sprites], col)
                if(col == 'p'):
                    self.player = Player((x, y))
                    self.visible_sprites.add(self.player)
                if(col == 'H'):
                    Tile((x,y),[self.visible_sprites,self.obstacles_sprites], col)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            dt = clock.tick(60)
            grid_data = [[1 if cell == ' ' else 0 for cell in row] for row in LEVEL1_GRIDMAP]
            grid = Grid(matrix=grid_data)  # Cria um novo grid a cada iteração

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return 'QUIT'  # retornar 'QUIT' para que o jogo termine 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print('mouse clicked')
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    if grid.node(pos[0]//TILESIZE, pos[1]//TILESIZE).walkable:
                        print("isWalkable")  # Correção para chamar o método walkable
                        self.player.move_to(pos, grid)
            self.visible_sprites.update()
            self.display_surface.blit(self.bg, (0, 0))
            self.visible_sprites.draw(self.display_surface)
            pygame.display.update()  # atualize a tela após desenhar os sprites

        return 'MAIN_MENU'