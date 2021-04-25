from __future__ import annotations

import pygame
from pygame.sprite import AbstractGroup

from appConstants import ImagesPath
#from casa import Casa
from pecas_models.pecaBase import PecaBase


class Peao(PecaBase):

    def __init__(self, *groups: AbstractGroup, rect_base: pygame.Rect, tom: str, posicao: tuple[int, int], casaOrigem: str):
        super().__init__(*groups, rect_base=rect_base, tom=tom, posicao=posicao, casaOrigem=casaOrigem)

        if self.tonalidade == 'escuro':
            self.caminho_imagem = ImagesPath.PEAO_PRETO
            self.valor = -1
        elif self.tonalidade == 'claro':
            self.caminho_imagem = ImagesPath.PEAO_BRANCO
            self.valor = 1

        self.carregar_imagem(self.rect.copy())

    def carregar_imagem(self, rect_base: pygame.Rect) -> None:
        self.image = pygame.image.load(self.caminho_imagem)
        self.image = pygame.transform.smoothscale(self.image, [self.rect.width, self.rect.height])

    def get_casas_possiveis(self, tabuleiro: list[list[Casa]], incluir_casas_ameacadas=False) -> list[Casa]:
        casas_possiveis: list[Casa] = []
        i: int = self.posicao[0]
        j: int = self.posicao[1]

        if self.tonalidade == 'claro':
            if i - 1 >= 0:
                if tabuleiro[i - 1][j].peca is None:
                    casas_possiveis.append(tabuleiro[i - 1][j])
                if self.movimentos == 0 and tabuleiro[i - 1][j].peca is None and tabuleiro[i - 2][j].peca is None:
                    casas_possiveis.append(tabuleiro[i - 2][j])
                if j - 1 >= 0:
                    if tabuleiro[i - 1][j - 1].peca is not None:
                        if tabuleiro[i - 1][j - 1].peca.tonalidade != self.tonalidade:
                            casas_possiveis.append(tabuleiro[i - 1][j - 1])
                if j + 1 < 8:
                    if tabuleiro[i - 1][j + 1].peca is not None:
                        if tabuleiro[i - 1][j + 1].peca.tonalidade != self.tonalidade:
                            casas_possiveis.append(tabuleiro[i - 1][j + 1])

            # Verificação en_passant peça clara
            linha = self.posicao[0]
            coluna = self.posicao[1]
            if linha == 3:
                # en_passant direita
                if coluna < 7:
                    if tabuleiro[linha][coluna + 1].peca is not None:
                        if type(tabuleiro[linha][coluna + 1].peca) == Peao and tabuleiro[linha][coluna + 1].peca.movimentos == 1:
                            casa_en_passant = (tabuleiro[linha - 1][coluna + 1])
                            casa_en_passant.is_en_passant = True
                            casas_possiveis.append(casa_en_passant)
                # en_passant esquerda
                if coluna > 0:
                    if tabuleiro[linha][coluna - 1].peca is not None:
                        if type(tabuleiro[linha][coluna - 1].peca) == Peao and tabuleiro[linha][coluna - 1].peca.movimentos == 1:
                            casa_en_passant = (tabuleiro[linha - 1][coluna - 1])
                            casa_en_passant.is_en_passant = True
                            casas_possiveis.append(casa_en_passant)


        elif self.tonalidade == 'escuro':
            if i + 1 < 8:
                if tabuleiro[i + 1][j].peca is None:
                    casas_possiveis.append(tabuleiro[i + 1][j])
                if self.movimentos == 0 and tabuleiro[i + 1][j].peca is None and tabuleiro[i + 2][j].peca is None:
                    casas_possiveis.append(tabuleiro[i + 2][j])
                if j - 1 >= 0:
                    if tabuleiro[i + 1][j - 1].peca is not None:
                        if tabuleiro[i + 1][j - 1].peca.tonalidade != self.tonalidade:
                            casas_possiveis.append(tabuleiro[i + 1][j - 1])
                if j + 1 < 8:
                    if tabuleiro[i + 1][j + 1].peca is not None:
                        if tabuleiro[i + 1][j + 1].peca.tonalidade != self.tonalidade:
                            casas_possiveis.append(tabuleiro[i + 1][j + 1])

            # Verificação en_passant peça escura
            linha = self.posicao[0]
            coluna = self.posicao[1]
            if linha == 4:
                # en_passant direita
                if coluna < 7:
                    if tabuleiro[linha][coluna + 1].peca is not None:
                        if type(tabuleiro[linha][coluna + 1].peca) == Peao and tabuleiro[linha][
                            coluna + 1].peca.movimentos == 1:
                            casa_en_passant = (tabuleiro[linha + 1][coluna + 1])
                            casa_en_passant.is_en_passant = True
                            casas_possiveis.append(casa_en_passant)
                # en_passant esquerda
                if coluna > 0:
                    if tabuleiro[linha][coluna - 1].peca is not None:
                        if type(tabuleiro[linha][coluna - 1].peca) == Peao and tabuleiro[linha][
                            coluna - 1].peca.movimentos == 1:
                            casa_en_passant = (tabuleiro[linha + 1][coluna - 1])
                            casa_en_passant.is_en_passant = True
                            casas_possiveis.append(casa_en_passant)

        return casas_possiveis

    def get_casas_de_captura(self, tabuleiro: list[list[Casa]]) -> list[Casa]:
        """
        Retorna as casas nas quais um Peão pode fazer uma captura.
        Função principalmente usada para um Rei conhecer as casas ameaçadas por um Peão.
        :param tabuleiro:
        :return:
        """
        casas_de_captura: list[Casa] = []
        i: int = self.posicao[0]
        j: int = self.posicao[1]

        if self.tonalidade == 'claro':
            if i - 1 >= 0:
                if j - 1 >= 0:
                    casas_de_captura.append(tabuleiro[i - 1][j - 1])
                if j + 1 < 8:
                    casas_de_captura.append(tabuleiro[i - 1][j + 1])

        elif self.tonalidade == 'escuro':
            if i + 1 < 8:
                if j - 1 >= 0:
                    casas_de_captura.append(tabuleiro[i + 1][j - 1])
                if j + 1 < 8:
                    casas_de_captura.append(tabuleiro[i + 1][j + 1])

        return casas_de_captura