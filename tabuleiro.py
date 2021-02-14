import pygame
from pygame.sprite import Group

from casa import Casa


class Tabuleiro:
    display: pygame.Surface
    objectGroup: Group
    vetorDeControle: list = []

    def __init__(
            self,
            display: pygame.Surface
    ):
        Tabuleiro.display = display
        Tabuleiro.altura_tela = display.get_height()
        Tabuleiro.objectGroup = pygame.sprite.Group()

    @staticmethod
    def desenharTabuleiro():
        for i in range(0, 8, 1):
            Tabuleiro.vetorDeControle.append([])
            for j in range(0, 8, 1):
                Tabuleiro.vetorDeControle[i].append(Casa(Tabuleiro.objectGroup,
                                                         display=Tabuleiro.display,
                                                         posicao_na_matriz=(i, j)))

        Tabuleiro.objectGroup.draw(Tabuleiro.display)
