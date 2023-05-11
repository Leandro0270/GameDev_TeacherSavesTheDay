import pygame
from tile import Tile
# Inicializa o pygame
class Level1:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        self.Level1_MOUSE_POS = pygame.mouse.get_pos()
        self.obstacles_sprites = pygame.sprite.Group()
        self.LEVEL1_GRIDMAP =[
            ['x','x','x','x','x','x','x','x','x','x','x','x'],
            ['x',' ','p',' ','x',' ',' ',' ',' ',' ',' ','x'],
            ['x',' ',' ',' ','x','e',' ',' ',' ',' ',' ','x'],
            ['x',' ',' ',' ','x','x',' ','x','x',' ',' ','x'],
            ['x',' ',' ',' ',' ',' ',' ',' ','x',' ',' ','x'],
            ['x','x','x','x','x',' ',' ',' ','x',' ',' ','x'],
            ['x',' ',' ',' ','x',' ',' ',' ','x',' ',' ','x'],
            ['x',' ',' ',' ','x',' ',' ',' ','x',' ',' ','x'],
            ['x',' ',' ',' ','x',' ',' ',' ','x',' ',' ','x'],
            ['x',' ',' ',' ','x','x','x','x','x',' ',' ','x'],
            ['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
            ['x','x','x','x','x','x','x','x','x','x','x','x']
        ]
        self.tileSize = 50;
        self.generateMap()

    def generateMap(self):
        for row_index,row in enumerate(self.LEVEL1_GRIDMAP):
            for col_index,col in enumerate(row):
                x = col_index * self.tileSize
                y = row_index * self.tileSize
                if(col == 'x'):
                    Tile((x,y),[self.visible_sprites])
                if(col == 'p'):
                    print('spawnPlayer')
                if(col == 'Ev'):
                    print('spawnEnemy in vertical patrol')
                if(col == 'EH'):
                    print('spawnEnemy in horizontal patrol')
    def run(self):
        self.visible_sprites.draw(self.display_surface)
