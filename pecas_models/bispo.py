from __future__ import annotations

import pygame
from pygame.sprite import AbstractGroup

from appConstants import ImagesPath
#from casa import Casa
from pecas_models.pecaBase import PecaBase


class Bispo(PecaBase):

    def __init__(self, *groups: AbstractGroup, rect_base: pygame.Rect, tom: str, posicao: tuple[int, int], casaOrigem: str):
        super().__init__(*groups, rect_base=rect_base, tom=tom, posicao=posicao, casaOrigem=casaOrigem)

        if self.tonalidade == 'escuro':
            self.caminho_imagem = ImagesPath.BISPO_PRETO
        elif self.tonalidade == 'claro':
            self.caminho_imagem = ImagesPath.BISPO_BRANCO

        self.carregar_imagem(self.rect.copy())

    def carregar_imagem(self, rect_base: pygame.Rect) -> None:
        self.image = pygame.image.load(self.caminho_imagem)
        self.image = pygame.transform.smoothscale(self.image, [self.rect.width, self.rect.height])

    def get_casas_possiveis(self, tabuleiro: list[list[Casa]]) -> list[tuple[int, int]]:
        casas_possiveis: list[Casa] = []
        i: int = self.posicao[0]
        j: int = self.posicao[1]

        #CÓDIGO
        casa_i = i
        casa_j = j
        casa_i_j_vazia = True  # proxima casa da variável i está vazia
        while (casa_i + 1 < 8) and (casa_j + 1 < 8) and casa_i_j_vazia:  # fica em loop enquanto a próxima casa está vazia ou encontrar uma peça do outro time
            if tabuleiro[casa_i + 1][casa_j + 1].peca is None:
                casas_possiveis.append(tabuleiro[casa_i + 1][casa_j + 1])
            elif self.tonalidade != tabuleiro[casa_i + 1][casa_j + 1].peca.tonalidade:
                casas_possiveis.append(tabuleiro[casa_i + 1][casa_j + 1])
                casa_i_j_vazia = False  # Próxima casa da variável i está com uma peça de cor diferente. Guarda a casa e sai do loop
            else:
                casa_i_j_vazia = False  # Próxima casa da variável i está com uma peça da mesma cor. Sai do loop
            casa_i += 1
            casa_j += 1
            print("i1", casa_i, "j1", casa_j)

        casa_i = i
        casa_j = j
        casa_i_j_vazia = True

        while (casa_i - 1 >= 0) and (casa_j - 1 >= 0) and casa_i_j_vazia:
            if tabuleiro[casa_i - 1][casa_j - 1].peca is None:
                casas_possiveis.append(tabuleiro[casa_i - 1][casa_j - 1])
            elif self.tonalidade != tabuleiro[casa_i - 1][casa_j - 1].peca.tonalidade:
                casas_possiveis.append(tabuleiro[casa_i - 1][casa_j - 1])
                casa_i_j_vazia = False
            else:
                casa_i_j_vazia = False
            casa_i -= 1
            casa_j -= 1
            print("i2", casa_i, "j2", casa_j)

        casa_j = j
        casa_i = i
        casa_i_j_vazia = True
        while (casa_j - 1 >= 0) and (casa_i + 1 < 8) and casa_i_j_vazia:
            if tabuleiro[casa_i + 1][casa_j - 1].peca is None:
                casas_possiveis.append(tabuleiro[casa_i + 1][casa_j - 1])
            elif self.tonalidade != tabuleiro[casa_i + 1][casa_j - 1].peca.tonalidade:
                casas_possiveis.append(tabuleiro[casa_i + 1][casa_j - 1])
                casa_i_j_vazia = False
            else:
                casa_i_j_vazia = False
            casa_j -= 1
            casa_i += 1
            print("i3", casa_i, "j3", casa_j)

        casa_j = j
        casa_i = i
        casa_i_j_vazia = True
        while (casa_j + 1 < 8) and (casa_i - 1 >= 0) and casa_i_j_vazia:
            if tabuleiro[casa_i - 1][casa_j + 1].peca is None:
                casas_possiveis.append(tabuleiro[casa_i - 1][casa_j + 1])
            elif self.tonalidade != tabuleiro[casa_i - 1][casa_j + 1].peca.tonalidade:
                casas_possiveis.append(tabuleiro[casa_i - 1][casa_j + 1])
                casa_i_j_vazia = False
            else:
                casa_i_j_vazia = False
            casa_j += 1
            casa_i -= 1
            print("i4", casa_i, "j4", casa_j)

        return casas_possiveis
