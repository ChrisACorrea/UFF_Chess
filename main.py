import pygame, pygame_menu

from appConstants import ImagesPath
from start import Start
from tabuleiro import Tabuleiro

# Inicializando Pygame
pygame.init()
# Criando a janela
display = pygame.display.set_mode([800, 600])

def modo_de_jogo(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    menu.disable()

menu = pygame_menu.Menu(600, 800, 'Bem vindo ao UFF_Chess',
                       theme=pygame_menu.themes.THEME_DARK)

menu.add.text_input('Nome do jogador 1 :', default='')
menu.add.text_input('Nome do jogador 2 :', default='')
menu.add.selector('Modo de jogo :', [('Jogador vs Jogador', 1), ('Jogador vs Máquina', 2)], onchange=modo_de_jogo)
menu.add.button('Jogar', start_the_game)
menu.add.button('Sair', pygame_menu.events.EXIT)
menu.mainloop(display)

# Trocando o título
windowIcon = pygame.image.load(ImagesPath.ICONE_PRETO)
pygame.display.set_caption("UFF Chess")
pygame.display.set_icon(windowIcon)

tabuleiro = Tabuleiro(display=display)
start = Start(display, tabuleiro)