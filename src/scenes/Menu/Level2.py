# Level2.py
import pygame
import random
from exit import Exit
from Level2Settings import *
from tile import Tile
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from player import Player 
from item import Item
from Ghost import Ghost
from UI import ui
from HUD import HUD
from student import student
class Level2:
    def __init__(self,game):
        self.game = game
        self.startCollectedItems = self.game.collectedItems
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()
        self.items_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()
        self.exit_sprites = pygame.sprite.Group()
        self.bg = pygame.image.load('level1BG.png').convert_alpha()
        self.dialogueSequence = 0
        self.itemSequenceText = 0
        self.generateMap()
        item = Item((310, 350), 'radio.png', ['Professor! Encontramos um rádio.'])
        item2 = Item((775,410), 'medkit.png', ['Olhem crianças, um kit médico!', 'Isso pode ser muito útil em casos de ferimentos durante uma evacuação.', 'Além disso pode ser que contenha pilulas de iodo,', 'que nos ajudam a evitar parte da radiação.'])
        self.items_sprites.add(item)
        self.items_sprites.add(item2)
        self.visible_sprites.add(item2)
        self.visible_sprites.add(item)
        self.canShowNextDialogue = False
        self.ui = ui(self.display_surface)
        self.hud = HUD(self.player, len(self.items_sprites), "Chegue ao final da fase", self.display_surface) 
        self.currentGhostPatrolIndex = 0
        self.ghost_respawn_timer = None
        self.ghost_killed = False

    def generateMap(self):
        self.patrol_points =[]
        for row_index,row in enumerate(LEVEL2_GRIDMAP):
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
                    self.companion1 = student((x, y), self.game, self.player,'marry.png', LEVEL2_GRIDMAP)
                    self.visible_sprites.add(self.companion1)
                if(col == 'c2'):
                    self.companion2 = student((x, y), self.game, self.player,'josh.png', LEVEL2_GRIDMAP)
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
        while running:
            dt = clock.tick(60)
            grid_data = [[0 if cell == 'x' or cell == 'H' else 1 for cell in row] for row in LEVEL2_GRIDMAP]
            grid = Grid(matrix=grid_data)
            if self.ui.showing_message:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        return 'QUIT'

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                        self.ui.hide_message()
                        if(self.canShowNextDialogue):
                            self.dialogueSequence += 1

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.ui.hide_message()
                        if(self.canShowNextDialogue):
                            self.dialogueSequence += 1

                
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
                        self.dialogueSequence += 1
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.ui.hide_dialogue()
                        self.dialogueSequence += 1
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

            if(self.dialogueSequence == 4):
                self.ui.show_dialogue(['Obrigado crianças, o rádio que vocês encontraram pode ser uma ferramenta', 
                                          'muito útil nessa situação. Vamos tentar contatar as autoridades e pedir', 
                                          'ajuda. Elas poderão fornecer orientações sobre como agir, lembrem-se de' ,
                                          'que as autoridades estão lá para ajudar e têm os recursos necessários', 
                                          'para lidar com esse tipo de situação.'], self.ui.playerDialogue)

            if(self.dialogueSequence == 0):
                self.ui.show_dialogue(['Professor, estamos com fome!'], self.ui.maryDialogue)
            

            if(self.dialogueSequence == 1):
                self.ui.show_dialogue(['E sede...'], self.ui.joshDialogue)
                

            if(self.dialogueSequence == 2):
                self.ui.show_dialogue(['Se acalmem, classe!',
                                  'Não comam nem bebam nada que esteja aqui e é essencial que vocês saibam por quê.', 
                                  'Após um acidente nuclear, pode haver contaminação em várias coisas ao nosso redor, como água,', 
                                  'alimentos e até mesmo em objetos que tocamos. Quando comemos ou bebemos algo contaminado pela ',
                                  'radiação, essa substância ruim entra em nosso corpo e isso podecausar sérios problemas de saúde.', 
                                  ], self.ui.playerDialogue)
            

            if(self.ghost.path == []):
                self.ghost.move_to(self.patrol_points[self.currentGhostPatrolIndex], grid)
                self.currentGhostPatrolIndex = (self.currentGhostPatrolIndex + 1) % len(self.patrol_points)
                
            if self.ghost.handle_collision_with_player(self.player):
                self.ghost.path = []  
                self.ghost.kill()
                pygame.time.set_timer(respawn_ghost_event, 3000)
            
            if self.player.isAlive == False:
                if(self.game.playerLivesRemaining > 0):
                    self.game.collectedItems = self.startCollectedItems
                    return 'LEVEL_2'
                else:
                    return 'GAME_OVER'


            for exit in self.exit_sprites:
                if exit.player_exit(self.player):
                    return 'LEVEL_3'
            collided_items = pygame.sprite.spritecollide(self.player, self.items_sprites, True)
            for item in collided_items:
                if(item.imageName == 'radio.png'):
                    self.canShowNextDialogue = True
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
