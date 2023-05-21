import pygame, sys
from Level1Settings import *
from button import Button
from Level1 import Level1

pygame.init()

SCREEN_WIDTH = 891
SCREEN_HEIGHT = 891


SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def options():
    while True:
        SCREEN.blit(BG, (0, 0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "white")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'QUIT'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return 'MAIN_MENU'

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(30).render("THE TEACHER SAVES THE DAY", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(440, 150))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(440, 250), 
                            text_input="PLAY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(440, 425), 
                            text_input="OPTIONS", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(440,600), 
                            text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'QUIT'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return 'LEVEL_1'
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return 'OPTIONS'
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return 'QUIT'

        pygame.display.update()

def game_loop():
    game_state = 'MAIN_MENU'

    while True:
        if game_state == 'MAIN_MENU':
            game_state = main_menu()
        elif game_state == 'LEVEL_1':
            game_state = Level1().run()
        elif game_state == 'OPTIONS':
            game_state = options()
        elif game_state == 'QUIT':
            pygame.quit()
            sys.exit()

        pygame.display.update()

game_loop()
