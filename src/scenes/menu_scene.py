import pygame
import pygame_menu

# Inicializa o Pygame
pygame.init()

# Configurações da tela
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


# Função de exemplo para quando um botão for clicado
def start_game():
    print("Iniciando o jogo...")

def options():
    print("Opções...")

def about():
    print("Sobre o jogo...")

def exit_game():
    print("Saindo do jogo...")
    pygame.quit()
    quit()

    
# Cria o menu
menu = pygame_menu.Menu('Menu Principal', screen_width, screen_height,
                       theme=pygame_menu.themes.THEME_BLUE)


# Adiciona botões ao menu
menu.add_button('Iniciar Jogo', start_game)
menu.add_button('Opções', options)
menu.add_button('Sobre', about)
menu.add_button('Sair', exit_game)


# Loop principal
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit_game()

    menu.mainloop(events)  # Atualiza o menu
    pygame.display.update()  # Atualiza a tela
