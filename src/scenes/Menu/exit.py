# exit.py
import pygame

class Exit(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.rect = pygame.Rect(pos[0], pos[1], 1, 1)  # Define um retângulo 1x1 invisível na posição especificada

    def player_exit(self, player):
        return pygame.sprite.collide_rect(self, player)  # Retorna True se o player estiver em contato com a saída
