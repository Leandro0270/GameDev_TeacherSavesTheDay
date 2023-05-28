# ui.py
import pygame

class ui:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)  # Fonte padrão, tamanho 24
        self.bg_color = (0, 0, 0)  # Cor de fundo do quadro: preto
        self.text_color = (255, 255, 255)  # Cor do texto: branco
        self.showing_message = False  
        self.showing_dialogue = False
        self.maryDialogue = pygame.image.load('maryDialogue.png')
        self.joshDialogue = pygame.image.load('joshDialogue.png')
        self.playerDialogue = pygame.image.load('TeacherDialogue.png')
        self.item_pick = pygame.mixer.Sound('soundEffects/itemSoundEffect.mp3')
        self.item = None

    def show_message(self, item):
        self.item_pick.play()
        self.showing_message = True
        self.item = item

    def hide_message(self):
        self.item_pick.play()
        self.showing_message = False
        self.item = None

    def update(self):
        if self.showing_message:
            self._draw_message(self.item)
        if self.showing_dialogue:
            self._draw_dialogue(self.dialogue, self.dialogueSpriteShow)

    def _draw_message(self, item):
        # Criação da caixa de texto
        text_box_width = 850
        text_box_height = 150
        line_height = self.font.get_linesize() * 1.5  # Aumenta o espaçamento entre as linhas em 50%
        text_box = pygame.Rect(0, 0, text_box_width, text_box_height)
        text_box.bottomleft = (20, self.screen.get_height() - 20)  # Posiciona a caixa de texto no canto inferior esquerdo

        # Criação do quadro de imagem
        image_box = pygame.Rect(0, 0, item.image.get_width(), item.image.get_height())
        image_box.topleft = (20, text_box.top - 20 - image_box.height)

        # Desenha o quadro na tela
        pygame.draw.rect(self.screen, self.bg_color, text_box)

        # Desenha cada linha de texto
        for i, line in enumerate(item.message):
            text_surface = self.font.render(line, True, self.text_color)
            line_pos = text_box.x + 10, text_box.y + 10 + i * line_height
            self.screen.blit(text_surface, line_pos)

        # Desenha o quadro de imagem e a imagem na tela
        pygame.draw.rect(self.screen, self.bg_color, image_box)
        self.screen.blit(item.image, (image_box.x, image_box.y))

    def hide_dialogue(self):
        self.showing_dialogue = False
        self.dialogue = None
        self.dialogueSpriteShow = None

    def show_dialogue(self, dialogue, spriteShow):
        self.dialogue = dialogue
        self.dialogueSpriteShow = spriteShow
        self.showing_dialogue = True

    def _draw_dialogue(self, dialogue, spriteShow):
        text_box_width = 850
        text_box_height = 150
        line_height = self.font.get_linesize() * 1.5  # Aumenta o espaçamento entre as linhas em 50%
        text_box = pygame.Rect(0, 0, text_box_width, text_box_height)
        text_box.bottomleft = (20, self.screen.get_height() - 20)  # Posiciona a caixa de texto no canto inferior esquerdo

        # Criação do quadro de imagem
        image_box = pygame.Rect(0, 0, spriteShow.get_width(), spriteShow.get_height())
        image_box.topleft = (20, text_box.top - 20 - image_box.height)

        # Desenha o quadro na tela
        pygame.draw.rect(self.screen, self.bg_color, text_box)

        # Desenha cada linha de texto
        for i, line in enumerate(dialogue):
            text_surface = self.font.render(line, True, self.text_color)
            line_pos = text_box.x + 10, text_box.y + 10 + i * line_height
            self.screen.blit(text_surface, line_pos)

        # Desenha o quadro de imagem e a imagem na tela
        pygame.draw.rect(self.screen, self.bg_color, image_box)
        self.screen.blit(spriteShow, (image_box.x, image_box.y))

    