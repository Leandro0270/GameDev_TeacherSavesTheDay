import pygame

# Inicializa o pygame
class Level1:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()
        self.Level1_MOUSE_POS = pygame.mouse.get_pos()
        self.obstacles_sprites = pygame.sprite.Group()

def run():
    pygame.init()
    pygame.display.set_caption("Level 1")

# Carrega uma tela branca
    image = pygame.image.load("../../../assets/background/backgroundTest.jpg")

    # Define o tamanho da célula
    cell_width = 50
    cell_height = 50

    # Calcula o número de células na grade
    grid_width = image.get_width() // cell_width
    grid_height = image.get_height() // cell_height

    # Cria a grade
    grid = []
    for i in range(grid_height):
        row = []
        for j in range(grid_width):
            # Calcula a posição e o tamanho do retângulo da célula
            rect = pygame.Rect(j*cell_width, i*cell_height, cell_width, cell_height)
            # Obtém a imagem da célula
            cell_image = image.subsurface(rect)
            # Adiciona a imagem da célula na linha
            row.append(cell_image)
        # Adiciona a linha na grade
        grid.append(row)

    # Cria uma janela para mostrar a imagem
    window = pygame.display.set_mode((image.get_width(), image.get_height()))

    # Loop principal
    running = True
    while running:

            # Desenha a grade na janela
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                window.blit(cell, (j*cell_width, i*cell_height))

            # Atualiza a janela
        pygame.display.flip()
