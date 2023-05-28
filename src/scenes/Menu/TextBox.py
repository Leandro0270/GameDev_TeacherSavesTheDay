import pygame
from pygame.locals import *

class TextBox:

    
    def __init__(self, rect, text_color=(255, 255, 255), font=None, limit=None):
        self.rect = pygame.Rect(rect)
        self.color = (0, 0, 0)  # Cor do retângulo ao redor da caixa de texto
        self.text_color = text_color  # Cor do texto
        self.text = ""  # O texto atualmente na caixa de texto
        self.font = pygame.font.Font(None, self.rect.height) if font is None else font
        self.limit = limit  # Limite do número de caracteres

    def update(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)  # Desenha a caixa de texto na superfície do Pygame
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))  # Desenha o texto na caixa de texto

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if self.limit is None or len(self.text) < self.limit:  # Verificar o limite antes de adicionar o caractere
                    self.text += event.unicode

    def draw(self, surface):
        surface.blit(self.rendered, (self.rect.x, self.rect.y))
        pygame.draw.rect(surface, self.color, self.rect, 2)  # desenha a borda do TextBox

    def get_text(self):
        return self.text
