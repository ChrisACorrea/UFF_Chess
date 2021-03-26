import pygame, pygame_menu

from appConstants import ImagesPath
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

gameLoop: bool = True
clock = pygame.time.Clock()

tabuleiro = Tabuleiro(display=display)

def draw():
    display.fill([46, 46, 46])

    tabuleiro.objectGroup.update()
    tabuleiro.desenhar_tabuleiro()

    pygame.display.update()


if __name__ == '__main__':
    while gameLoop:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                posicao_mouse = pygame.mouse.get_pos()
                if tabuleiro.clicou_dentro_do_tabuleiro(posicao_mouse):
                    tabuleiro.selecionar_casa(posicao_mouse)
                else:
                    tabuleiro.limpar_selecoes()

        draw()
