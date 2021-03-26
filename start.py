import pygame
from appConstants import ImagesPath
from tabuleiro import Tabuleiro
from pygame import font
import time

class Start():
    def draw(self, display, tabuleiro):
        display.fill([46, 46, 46])

        tabuleiro.objectGroup.update()
        tabuleiro.desenhar_tabuleiro()

        pygame.display.update()

    def __init__(self, display, tabuleiro):
        gameLoop: bool = True
        clock = pygame.time.Clock()

        if __name__ == 'start':
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
                self.draw(display, tabuleiro)

