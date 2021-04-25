import pygame, pygame_menu

from appConstants import ImagesPath
from start import Start
from tabuleiro import Tabuleiro

# Inicializando Pygame
pygame.init()
# Criando a janela
display = pygame.display.set_mode([1280, 720])

modoJogo = 1

def modo_de_jogo(value, difficulty):
    print(value)
    tipo, valor = value
    print(tipo)
    modo, valor = tipo
    global modoJogo
    modoJogo = valor
    pass

menu = pygame_menu.Menu(720, 1280, 'Bem vindo ao UFF_Chess',
                       theme=pygame_menu.themes.THEME_DARK)

jogador1 = menu.add.text_input('Nome do jogador 1: ', default='')
jogador2 = menu.add.text_input('Nome do jogador 2: ', default='')
menu.add.selector('Modo de jogo :', [('Jogador vs Jogador', 1), ('Jogador vs IA', 2)], onchange=modo_de_jogo)
menu.add.button('Jogar', menu.disable)
menu.add.button('Sair', pygame_menu.events.EXIT)
menu.mainloop(display)


# Trocando o título
windowIcon = pygame.image.load(ImagesPath.ICONE_PRETO)
pygame.display.set_caption("UFF Chess")
pygame.display.set_icon(windowIcon)
jogador1 = jogador1.get_value()
jogador2 = jogador2.get_value()
tabuleiro = Tabuleiro(display=display, jogador1=jogador1, jogador2=jogador2, modo_de_jogo = modoJogo)
start = Start(display, tabuleiro)