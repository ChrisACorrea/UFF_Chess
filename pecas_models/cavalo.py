from __future__ import annotations

import pygame
from pygame.sprite import AbstractGroup

from appConstants import ImagesPath
#from casa import Casa
from pecas_models.pecaBase import PecaBase


class Cavalo(PecaBase):

    def __init__(self, *groups: AbstractGroup, rect_base: pygame.Rect, tom: str, posicao: tuple[int, int], casaOrigem: str):
        super().__init__(*groups, rect_base=rect_base, tom=tom, posicao=posicao, casaOrigem=casaOrigem)

        if self.tonalidade == 'escuro':
            self.caminho_imagem = ImagesPath.CAVALO_PRETO
            self.valor = -3
        elif self.tonalidade == 'claro':
            self.caminho_imagem = ImagesPath.CAVALO_BRANCO
            self.valor = 3

        self.carregar_imagem(self.rect.copy())

    def carregar_imagem(self, rect_base: pygame.Rect) -> None:
        self.image = pygame.image.load(self.caminho_imagem)
        self.image = pygame.transform.smoothscale(self.image, [self.rect.width, self.rect.height])

    def get_casas_possiveis(self, tabuleiro: list[list[Casa]], incluir_casas_ameacadas=False) -> list[Casa]:
        casas_possiveis: list[Casa] = []
        i: int = self.posicao[0]
        j: int = self.posicao[1]

        if (i - 2 >= 0) and (j - 1 >= 0):
            if tabuleiro[i - 2][j - 1].peca is None:
                casas_possiveis.append(tabuleiro[i - 2][j - 1])
            elif (self.tonalidade != tabuleiro[i - 2][j - 1].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i - 2][j - 1])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i - 2][j - 1])
        
        if (i - 2 >= 0) and (j + 1 < 8):
            if tabuleiro[i - 2][j + 1].peca is None:
                casas_possiveis.append(tabuleiro[i - 2][j + 1])
            elif (self.tonalidade != tabuleiro[i - 2][j + 1].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i - 2][j + 1])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i - 2][j + 1])
        
        if (i - 1 >= 0) and (j - 2 >= 0):
            if tabuleiro[i - 1][j - 2].peca is None:
                casas_possiveis.append(tabuleiro[i - 1][j - 2])
            elif (self.tonalidade != tabuleiro[i - 1][j - 2].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i - 1][j - 2])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i - 1][j - 2])

        if (i - 1 >= 0) and (j + 2 < 8):
            if tabuleiro[i - 1][j + 2].peca is None:
                casas_possiveis.append(tabuleiro[i - 1][j + 2])
            elif (self.tonalidade != tabuleiro[i - 1][j + 2].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i - 1][j + 2])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i - 1][j + 2])

        if (i + 1 < 8) and (j - 2 >= 0):
            if tabuleiro[i + 1][j - 2].peca is None:
                casas_possiveis.append(tabuleiro[i + 1][j - 2])
            elif (self.tonalidade != tabuleiro[i + 1][j - 2].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i + 1][j - 2])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i + 1][j - 2])

        if (i + 1 < 8) and (j + 2 < 8):
            if tabuleiro[i + 1][j + 2].peca is None:
                casas_possiveis.append(tabuleiro[i + 1][j + 2])
            elif (self.tonalidade != tabuleiro[i + 1][j + 2].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i + 1][j + 2])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i + 1][j + 2])

        if (i + 2 < 8) and (j - 1 >= 0):
            if tabuleiro[i + 2][j - 1].peca is None:
                casas_possiveis.append(tabuleiro[i + 2][j - 1])
            elif (self.tonalidade != tabuleiro[i + 2][j - 1].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i + 2][j - 1])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i + 2][j - 1])

        if (i + 2 < 8) and (j + 1 < 8):
            if tabuleiro[i + 2][j + 1].peca is None:
                casas_possiveis.append(tabuleiro[i + 2][j + 1])
            elif (self.tonalidade != tabuleiro[i + 2][j + 1].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i + 2][j + 1])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i + 2][j + 1])

        return casas_possiveis
