# Level1.py
import pygame
import random
from Level1Settings import *
from tile import Tile
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from player import Player 
from item import Item
from Ghost import Ghost
from UI import ui
from HUD import HUD


def find_path(grid_map, start, end):
    grid = Grid(matrix=grid_map)
    start = grid.node(start[0], start[1])
    end = grid.node(end[0], end[1])

    finder = AStarFinder()
    path, _ = finder.find_path(start, end, grid)

    nodes_path = [(node.x, node.y) for node in path]
    return nodes_path



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
        
        #objetivo nivel 2 = Sobreviva até o final e nível 3 = Evacue o prédio
        
        self.currentGhostPatrolIndex = 0



    def generateMap(self):
            self.patrol_points =[]
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
                    if(col == 'es'):
                        self.patrol_points.append((x, y))
                        self.ghost = Ghost((x, y), 2, (x, y))
                        self.enemies_sprites.add(self.ghost)
                        self.visible_sprites.add(self.ghost)
                        
                    if(col == 'ep'):
                        self.patrol_points.append((x, y))


    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            dt = clock.tick(60)
            grid_data = [[0 if cell == 'x' or cell == 'H' else 1 for cell in row] for row in LEVEL1_GRIDMAP]
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


            if(self.ghost.path == []):
                self.ghost.move_to(self.patrol_points[self.currentGhostPatrolIndex], grid)
                self.currentGhostPatrolIndex = (self.currentGhostPatrolIndex + 1) % len(self.patrol_points)
                
            if self.ghost.handle_collision_with_player(self.player):
                    self.ghost.path = []          

            collided_items = pygame.sprite.spritecollide(self.player, self.items_sprites, True)
            for item in collided_items:
                self.ui.show_message(item)
                self.hud.item_collected()

            self.visible_sprites.update()
            self.ui.update()
            self.hud.update()
            self.display_surface.blit(self.bg, (0, 0))
            self.visible_sprites.draw(self.display_surface)
            pygame.display.update()

        return 'MAIN_MENU'
    


        
