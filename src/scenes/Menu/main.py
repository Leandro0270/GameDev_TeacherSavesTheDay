import pygame, sys
from Level1Settings import *
from button import Button
from Level1 import Level1
from Level2 import Level2
from Level3 import Level3
from TextBox import TextBox
import csv
import time

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 891
SCREEN_HEIGHT = 925


SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.gif")
BG2 = pygame.image.load("assets/Background.png")

class Game:
    def __init__(self):
        self.start_time = time.time()
        self.isMusicOn = True
        self.playerLifePoints = 100
        self.playerLivesRemaining = 3
        self.collectedItems = 0
        self.playerTime = 0
game = Game()
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play_music(music_file, LoopingIndex):
    if pygame.mixer.music.get_busy():  # Se música está tocando
        pygame.mixer.music.stop()  # Para a música
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(LoopingIndex)


def toggle_music():
    if pygame.mixer.music.get_busy():  # Se música está tocando
        pygame.mixer.music.stop()  # Para a música
        game.isMusicOn = False
    else:
        pygame.mixer.music.play(-1)
        game.isMusicOn = True


def splash_screen():
    logo = pygame.image.load('mackenzie.png')
    start_ticks = pygame.time.get_ticks()

    fade_duration = 2000  # duração do fade em milissegundos
    logo_duration = 3000  # duração da logo na tela em milissegundos

    while True:
        SCREEN.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'QUIT'

        elapsed_time = pygame.time.get_ticks() - start_ticks

        if elapsed_time > logo_duration + fade_duration:  # logo já totalmente desaparecido
            return 'MAIN_MENU'
        elif elapsed_time > logo_duration:  # início do fade
            alpha = max(255 - ((elapsed_time - logo_duration) / fade_duration * 255), 0)  # calcular a opacidade
            logo.set_alpha(alpha)

        SCREEN.blit(logo, (SCREEN_WIDTH // 2 - logo.get_width() // 2, SCREEN_HEIGHT // 2 - logo.get_height() // 2))

        pygame.display.update()
        pygame.time.delay(10)
def options():
    # Definir uma variável que vai controlar se as instruções estão sendo exibidas ou não
    show_how_to_play = False

    while True:
        SCREEN.blit(BG, (0, 0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        overlay = pygame.Surface((770, 700))
        overlay.set_alpha(200)  # alpha range is 0-255, so 64 is roughly 25%

        # Preencha a superfície com preto
        overlay.fill('black')

        # Desenhe a superfície na tela
        SCREEN.blit(overlay, (60, 80))
        HOW_TO_PLAY_BUTTON = Button(image=None, pos=(440, 260), 
                            text_input="Como jogar", font=get_font(30), base_color="White", hovering_color="Green")
        TOGGLE_MUSIC_BUTTON = Button(image=None, pos=(440, 360), 
                            text_input="Ligar/Desligar Música", font=get_font(30), base_color="White", hovering_color="Green")
        OPTIONS_BACK = Button(image=None, pos=(440, 460), 
                            text_input="Voltar", font=get_font(30), base_color="White", hovering_color="Green")
        RETURN_BUTTON = Button(image=None, pos=(440, 500), 
                            text_input="Voltar", font=get_font(30), base_color="White", hovering_color="Green")

        if show_how_to_play:
            

            instructions = [
                "Objetivo:",
                "-Colete todo os itens para ganhar mais pontos",
                "-Evite os fantasmas da radiação",
                "-Chegue a saida para passar de nivel",
                "",
                "Comandos: Clique do mouse esquerdo para movimentar"
            ]
            
            for i, line in enumerate(instructions):
                OPTIONS_TEXT = get_font(15).render(line, True, "white")
                OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(440, 160 + 40 * i))
                SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
            RETURN_BUTTON.changeColor(OPTIONS_MOUSE_POS)
            RETURN_BUTTON.update(SCREEN)
        else:
            for button in [HOW_TO_PLAY_BUTTON, TOGGLE_MUSIC_BUTTON, OPTIONS_BACK]:
                button.changeColor(OPTIONS_MOUSE_POS)
                button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'QUIT'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return 'MAIN_MENU'
                elif HOW_TO_PLAY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    # Toggle the instructions when the HOW_TO_PLAY_BUTTON is clicked
                    show_how_to_play = True
                elif TOGGLE_MUSIC_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    # Toggle the music when the TOGGLE_MUSIC_BUTTON is clicked
                    toggle_music()
                elif RETURN_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    # Toggle the instructions when the RETURN_BUTTON is clicked
                    show_how_to_play = False

        pygame.display.update()
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(30).render("THE TEACHER SAVES THE DAY", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(440, 150))

        # Crie uma nova superfície com o mesmo tamanho que a tela
        overlay = pygame.Surface((770, 700))

        # Ajuste a opacidade da superfície (85% opaco significa 25.5% transparente)
        overlay.set_alpha(200)  # alpha range is 0-255, so 64 is roughly 25%

        # Preencha a superfície com preto
        overlay.fill('black')

        # Desenhe a superfície na tela
        SCREEN.blit(overlay, (60, 80))

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
                    game.playerLifePoints = 100
                    game.playerLivesRemaining = 3
                    game.collectedItems = 0
                    game.start_time = pygame.time.get_ticks()
                    return 'LEVEL_1'
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return 'OPTIONS'
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return 'QUIT'

        pygame.display.update()

def save_score(initials, time):
    with open('scores.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([initials, time])

def victory_screen():
    game.playerTime = (pygame.time.get_ticks() - game.start_time) / 1000  # Parar o cronômetro
    initials = ""
    text_box = TextBox((600, 480, 140, 30), limit=3)



    while True:
        SCREEN.blit(BG2, (0, 0))

        VICTORY_MOUSE_POS = pygame.mouse.get_pos()

        VICTORY_TITLE = get_font(30).render("Você salvou as crianças!", True, "Green")
        VICTORY_TITLE_RECT = VICTORY_TITLE.get_rect(center=(440, 150))

        stats = [
            f"Pontos de vida restantes: {game.playerLifePoints}",
            f"Vidas restantes: {game.playerLivesRemaining}",
            f"Itens coletados: {game.collectedItems} / 5",
            f"Tempo para terminar o jogo: {game.playerTime} segundos"
        ]

        for i, line in enumerate(stats):
            STATS_TEXT = get_font(15).render(line, True, "white")
            STATS_RECT = STATS_TEXT.get_rect(center=(440, 200 + 40 * i))
            SCREEN.blit(STATS_TEXT, STATS_RECT)
        INITIALS_PROMPT_TEXT = get_font(15).render('Insira suas iniciais:', True, "White")
        INITIALS_PROMPT_RECT = INITIALS_PROMPT_TEXT.get_rect(center=(440, 500))
         
        SCREEN.blit(INITIALS_PROMPT_TEXT, INITIALS_PROMPT_RECT)

        text_box.update(SCREEN)

        SCORE_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(440, 600), 
                            text_input="Continuar", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(VICTORY_TITLE, VICTORY_TITLE_RECT)

        SCORE_BUTTON.changeColor(VICTORY_MOUSE_POS)
        SCORE_BUTTON.update(SCREEN)
        
        for event in pygame.event.get():
            initials = text_box.text
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Se a tecla Enter for pressionada
                    initials = text_box.text
                    save_score(initials, game.playerTime)  # Salvar a pontuação
                    return 'SCORE_BOARD'
            if event.type == pygame.QUIT:
                return 'QUIT'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SCORE_BUTTON.checkForInput(VICTORY_MOUSE_POS):
                    if(initials != ""):
            
                        save_score(initials, game.playerTime)
                        return 'SCORE_BOARD'
            text_box.handle_event(event)

        pygame.display.update()

def get_top_scores():
    try:
        with open('scores.csv', 'r') as file:
            scores = list(csv.reader(file))

        scores = [(score[0], float(score[1])) for score in scores if float(score[1]) >= 0]

        scores.sort(key=lambda score: score[1])

    
        return scores[:5]

    except FileNotFoundError:
    
        return []

def high_scores_screen():
    while True:
        SCREEN.blit(BG2, (0, 0))
        MENU_TEXT = get_font(30).render("Melhores tempos", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(440, 150))
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        scores = get_top_scores()

        for i, score in enumerate(scores):
            score_text = get_font(20).render(f"{score[0]}: {score[1]}", True, "white")
            score_rect = score_text.get_rect(center=(440, 200 + 40 * i))
            SCREEN.blit(score_text, score_rect)

        MENU_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(440, 600), 
                                text_input="MENU", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        MOUSE_POS = pygame.mouse.get_pos()
        MENU_BUTTON.changeColor(MOUSE_POS)
        MENU_BUTTON.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'QUIT'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BUTTON.checkForInput(MOUSE_POS):
                    return 'MAIN_MENU'
                
        pygame.display.update()

def game_over():
    while True:
        SCREEN.blit(BG, (0, 0))

        OVER_MOUSE_POS = pygame.mouse.get_pos()

        OVER_TEXT = get_font(30).render("GAME OVER", True, "Red")
        OVER_RECT = OVER_TEXT.get_rect(center=(440, 150))

        RETRY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(440, 250), 
                            text_input="RETRY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        MENU_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(440, 425), 
                            text_input="MENU", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(440,600), 
                            text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(OVER_TEXT, OVER_RECT)

        for button in [RETRY_BUTTON, MENU_BUTTON, QUIT_BUTTON]:
            button.changeColor(OVER_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'QUIT'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RETRY_BUTTON.checkForInput(OVER_MOUSE_POS):
                    game.playerLifePoints = 100
                    game.playerLivesRemaining = 3
                    game.collectedItems = 0
                    game.start_time = pygame.time.get_ticks()
                    return 'LEVEL_1'
                if MENU_BUTTON.checkForInput(OVER_MOUSE_POS):
                    return 'MAIN_MENU'
                if QUIT_BUTTON.checkForInput(OVER_MOUSE_POS):
                    return 'QUIT'

        pygame.display.update()

def game_loop():
    game_state = 'SPLASH'
    while True:
        if game_state == 'SPLASH':
            play_music('songs/startup.mp3', 1)
            game_state = splash_screen()
        if game_state == 'MAIN_MENU':
            if(game.isMusicOn == True):
                play_music('songs/menuSong.mp3', -1)
            game.playerLifePoints = 100
            game.playerLivesRemaining = 3
            game_state = main_menu()
        elif game_state == 'LEVEL_1':
            if(game.isMusicOn == True):
                play_music('songs/Level1.mp3', -1)
            game_state = Level1(game).run()
        elif game_state == 'LEVEL_2':
            game_state = Level2(game).run()
        elif game_state == 'LEVEL_3':
            game_state = Level3(game).run()
        elif game_state == 'OPTIONS':
            game_state = options()
        elif game_state == 'GAME_OVER':
            if(game.isMusicOn == True):
                play_music('songs/gameOverSong.mp3', 1)
            game.playerLifePoints = 100
            game.playerLivesRemaining = 3
            game_state = game_over()
        elif game_state == 'VICTORY':
            if(game.isMusicOn == True):
                play_music('songs/victorySong.mp3', 1)
            game_state = victory_screen()
        elif game_state == 'SCORE_BOARD':
            game_state = high_scores_screen()
        elif game_state == 'QUIT':
            pygame.quit()
            sys.exit()

        pygame.display.update()

game_loop()
