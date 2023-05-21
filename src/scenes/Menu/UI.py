# ui.py
import pygame

class ui:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)  # Fonte padrão, tamanho 24
        self.bg_color = (0, 0, 0)  # Cor de fundo do quadro: preto
        self.text_color = (255, 255, 255)  # Cor do texto: branco
        self.showing_message = False  # Adiciona um estado para mostrar ou não a mensagem
        self.item = None

    def show_message(self, item):
        self.showing_message = True
        self.item = item

    def hide_message(self):
        self.showing_message = False
        self.item = None

    def update(self):
        if self.showing_message:
            self._draw_message(self.item)

    def _draw_message(self, item):
        # Criação da superfície do texto
        text_surface = self.font.render(item.message, True, self.text_color)
        # Criação da caixa de texto
        text_box = pygame.Rect(0, 0, self.screen.get_width() / 2, text_surface.get_height() * 2)
        text_box.bottomleft = (20, self.screen.get_height() - 20)  # Posiciona a caixa de texto no canto inferior esquerdo
        # Criação do quadro de imagem
        image_box = pygame.Rect(0, 0, item.image.get_width(), item.image.get_height())
        image_box.topleft = (20, text_box.top - 20 - image_box.height)
        # Desenha o quadro e o texto na tela
        pygame.draw.rect(self.screen, self.bg_color, text_box)
        self.screen.blit(text_surface, (text_box.x + 10, text_box.y + 10))  # Posiciona o texto com um pequeno padding dentro da caixa de texto
        # Desenha o quadro de imagem e a imagem na tela
        pygame.draw.rect(self.screen, self.bg_color, image_box)
        self.screen.blit(item.image, (image_box.x, image_box.y))
