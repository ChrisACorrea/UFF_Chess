import pygame

from appConstants import ImagesPath
from tabuleiro import Tabuleiro

# Inicializando Pygame
pygame.init()
# Criando a janela
display = pygame.display.set_mode([800, 600])
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
