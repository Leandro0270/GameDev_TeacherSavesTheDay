# player.py
import pygame
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from Level1Settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, game):
        super().__init__()
        self.startPosition = pos
        self.game = game
        self.life = 100
        self.lives = 3
        self.default_image = pygame.image.load('player.png')
        self.hit_image = pygame.image.load('playerHit.png')
        self.image = self.default_image
        self.rect = self.image.get_rect(center=pos)
        self.speed = 100
        self.path = []
        self.isAlive = True
        self.damage_sound = pygame.mixer.Sound('soundEffects/playerHit.mp3')
        self.last_update = pygame.time.get_ticks()
        self.last_hit_time = None

    def update(self):
        now = pygame.time.get_ticks()
        if self.path and now - self.last_update > self.speed:
            next_pos = self.path[0]
            self.rect.topleft = (next_pos[0]*TILESIZE, next_pos[1]*TILESIZE)
            self.path = self.path[1:]
            self.last_update = now

        # se o jogador foi atingido nos últimos 2 segundos, fazê-lo piscar
        if self.last_hit_time and now - self.last_hit_time < 1000:
            if self.image == self.default_image:
                self.image = self.hit_image
            else:
                self.image = self.default_image
        else:
            self.image = self.default_image

    def move_to(self, pos, grid):
        start = grid.node(self.rect.x // TILESIZE, self.rect.y // TILESIZE)
        end = grid.node(pos[0] // TILESIZE, pos[1] // TILESIZE)
        finder = AStarFinder()
        path, runs = finder.find_path(start, end, grid)

        if path:
            self.path = path[1:]

    def take_damage(self, damage):
        self.damage_sound.play()
        self.life -= damage
        self.game.playerLifePoints = self.life
        self.last_hit_time = pygame.time.get_ticks()  # registra quando o jogador foi atingido
        if self.life <= 0:
            self.game.playerLivesRemaining -= 1
            self.game.playerLifePoints = 100
            self.isAlive = False
