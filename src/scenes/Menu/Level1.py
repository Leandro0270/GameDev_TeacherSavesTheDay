# Level1.py
import pygame
from Level1Settings import *
from tile import Tile
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from player import Player 
from item import Item
from Ghost import Ghost
from UI import ui
from HUD import HUD

class Level1:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        self.items_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()
        self.bg = pygame.image.load('level1BG.png').convert_alpha()
        self.generateMap()
        item = Item((500, 100), 'oxigenio.png', 'Você pegou o item!')
        self.items_sprites.add(item)
        self.visible_sprites.add(item)
        self.ui = ui(self.display_surface)
        self.hud = HUD(self.player, len(self.items_sprites), "Chegue ao final da fase", self.display_surface)


    def generateMap(self):
        for row_index,row in enumerate(LEVEL1_GRIDMAP):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if(col == 'x'):
                    Tile((x,y),[self.visible_sprites,self.obstacles_sprites], col)
                if(col == 'p'):
                    print("Instanciou o player")
                    print(x)
                    print(y)
                    self.player = Player((x, y))
                    print(self.player)
                    self.visible_sprites.add(self.player)
                if(col == 'H'):
                    Tile((x,y),[self.visible_sprites,self.obstacles_sprites], col)
                if(col == 'es'):
                    self.ghost = Ghost((x, y), 'ghost.png', 2, LEVEL1_GRIDMAP, TILESIZE)
                    self.enemies_sprites.add(self.ghost)
                

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            dt = clock.tick(60)
            grid_data = [[1 if cell == ' ' or cell == 'p' or cell=='es' or cell=='ep' else 0 for cell in row] for row in LEVEL1_GRIDMAP]
            grid = Grid(matrix=grid_data)

            if self.ui.showing_message:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        return 'QUIT'

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                        self.ui.hide_message()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.ui.hide_message()
                
                self.ui.update()
                pygame.display.update()
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return 'QUIT'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print('mouse clicked')
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    if grid.node(pos[0]//TILESIZE, pos[1]//TILESIZE).walkable:
                        print("isWalkable")
                        self.player.move_to(pos, grid)

            # Atualizando Ghost
            if pygame.sprite.collide_rect(self.player, self.ghost):
                self.player.take_damage(50)
                self.ghost.reset_position()

            # Verifica se o player colidiu com algum item
            collided_items = pygame.sprite.spritecollide(self.player, self.items_sprites, True)
            for item in collided_items:
                self.ui.show_message(item)
                self.hud.item_collected()

            self.visible_sprites.update()
            self.ui.update()
            self.hud.update()
            self.display_surface.blit(self.bg, (0, 0))
            self.enemies_sprites.draw(self.display_surface)
            self.visible_sprites.draw(self.display_surface)
            pygame.display.update()

        return 'MAIN_MENU'