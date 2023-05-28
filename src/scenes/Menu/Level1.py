# Level1.py
import pygame
import random
from exit import Exit
from Level1Settings import *
from tile import Tile
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from player import Player 
from item import Item
from Ghost import Ghost
from UI import ui
from HUD import HUD
from student import student
class Level1:
    def __init__(self,game):
        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        self.items_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()
        self.exit_sprites = pygame.sprite.Group()
        self.bg = pygame.image.load('level1BG.png').convert_alpha()
        self.generateMap()
        textoOxigenio = ['Crianças, atenção!', 
                         'Após um acidente nuclear, pode haver substâncias perigosas no ar, chamadas de radiação, que ',
                         'podem prejudicar nossa saúde se as respirarmos. É por isso que usamos máscaras e oxigênio.', 'Também usamos trajes de proteção para proteger nosso corpo da radiação. Eles são feitos de', 
                         'materiais especiais que bloqueiam a radiação e impedem que ela entre em contato com nossa pele.'
        ]
        item = Item((500, 100), 'oxigenio.png', textoOxigenio)
        item2 = Item((800, 400), 'geiger.png', ['Classe, este aqui é um contador geiger!', 'Podemos usá-lo para medir a quantidade de radiação no ar.', 'Quanto mais radiação, mais rápido o contador geiger apita!'])
        self.dialogueIndex = 0
        self.items_sprites.add(item)
        self.visible_sprites.add(item)
        self.items_sprites.add(item2)
        self.visible_sprites.add(item2)
        self.canShowNextDialogue = False
        self.ui = ui(self.display_surface)
        self.hud = HUD(self.player, len(self.items_sprites), "Chegue ao final da fase", self.display_surface) 
        self.currentGhostPatrolIndex = 0
        self.ghost_respawn_timer = None
        self.ghost_killed = False

    def generateMap(self):
        self.patrol_points =[]
        for row_index,row in enumerate(LEVEL1_GRIDMAP):
            for col_index,col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                
                if(col == 'x'):
                    Tile((x,y),[self.visible_sprites,self.obstacles_sprites], col)
                if(col == 'p'):
                    self.player = Player((x, y), self.game)
                    self.player.lives = self.game.playerLivesRemaining
                    self.player.life = self.game.playerLifePoints
                    self.visible_sprites.add(self.player)
                if(col == 'c1'):
                    self.companion1 = student((x, y), self.game, self.player,'marry.png', LEVEL1_GRIDMAP)
                    self.visible_sprites.add(self.companion1)
                if(col == 'c2'):
                    self.companion2 = student((x, y), self.game, self.player,'josh.png', LEVEL1_GRIDMAP)
                    self.visible_sprites.add(self.companion2)
                if(col == 'H'):
                    Tile((x,y),[self.visible_sprites,self.obstacles_sprites], col)
                if(col == 'es'):
                    self.ghost = Ghost((x, y), 2, (x, y))
                    self.enemies_sprites.add(self.ghost)
                    self.visible_sprites.add(self.ghost)
                if(col == 'ep'):
                    self.patrol_points.append((x, y))
                if(col == 's'):
                    exit = Exit((x, y))  # Cria uma saída na posição x, y
                    self.exit_sprites.add(exit)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        respawn_ghost_event = pygame.USEREVENT + 1
        self.ui.show_dialogue(['Calma, garotada!', 'Fiquem todos juntos, me sigam e sem brigar!'], self.ui.playerDialogue)

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
               
            if self.ui.showing_dialogue:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        return 'QUIT'

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                        self.ui.hide_dialogue()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.ui.hide_dialogue()
        
                self.visible_sprites.update()
                self.display_surface.blit(self.bg, (0, 0))
                self.visible_sprites.draw(self.display_surface)
                self.ui.update()
                pygame.display.update()
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return 'QUIT'
                elif event.type == respawn_ghost_event:
                    if not self.ghost.alive():  # If the ghost is not already in the game
                        self.ghost.respawn()
                        self.visible_sprites.add(self.ghost)
                        self.enemies_sprites.add(self.ghost)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if grid.node(pos[0]//TILESIZE, pos[1]//TILESIZE).walkable:
                        self.player.move_to(pos, grid)


            if(self.ghost.path == []):
                self.ghost.move_to(self.patrol_points[self.currentGhostPatrolIndex], grid)
                self.currentGhostPatrolIndex = (self.currentGhostPatrolIndex + 1) % len(self.patrol_points)
                
            if self.ghost.handle_collision_with_player(self.player):
                self.ghost.path = []  
                self.ghost.kill()
                pygame.time.set_timer(respawn_ghost_event, 3000)
            
            for exit in self.exit_sprites:
                if exit.player_exit(self.player):
                    return 'LEVEL_2'

            if self.player.isAlive == False:
                if(self.game.playerLivesRemaining > 0):
                    self.game.collectedItems = 0
                    return 'LEVEL_1'
                else:
                    return 'GAME_OVER'

            collided_items = pygame.sprite.spritecollide(self.player, self.items_sprites, True)
            for item in collided_items:
                self.game.collectedItems += 1
                self.ui.show_message(item)
                self.hud.item_collected()

            self.visible_sprites.update()
            self.ui.update()
        
            self.display_surface.blit(self.bg, (0, 0))
            self.visible_sprites.draw(self.display_surface)
            self.hud.update()

            pygame.display.update()

        return 'MAIN_MENU'
