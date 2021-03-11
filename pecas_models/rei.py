from __future__ import annotations

import pygame
from pygame.sprite import AbstractGroup

from appConstants import ImagesPath
#from casa import Casa
from pecas_models.pecaBase import PecaBase

from pecas_models.bispo import Bispo

from pecas_models.cavalo import Cavalo

from pecas_models.peao import Peao

from pecas_models.rainha import Rainha

from pecas_models.torre import Torre


class Rei(PecaBase):

    def __init__(self, *groups: AbstractGroup, rect_base: pygame.Rect, tom: str, posicao: tuple[int, int], casaOrigem: str):
        super().__init__(*groups, rect_base=rect_base, tom=tom, posicao=posicao, casaOrigem=casaOrigem)
        if self.tonalidade == 'escuro':
            self.caminho_imagem = ImagesPath.REI_PRETO
        elif self.tonalidade == 'claro':
            self.caminho_imagem = ImagesPath.REI_BRANCO

        self.carregar_imagem(self.rect.copy())

    def carregar_imagem(self, rect_base: pygame.Rect) -> None:
        self.image = pygame.image.load(self.caminho_imagem)
        self.image = pygame.transform.smoothscale(self.image, [self.rect.width, self.rect.height])

    def get_casas_possiveis(self, tabuleiro: list[list[Casa]]) -> list[tuple[int, int]]:
        
        i: int = self.posicao[0]
        j: int = self.posicao[1]

        if (self.tonalidade == 'claro'):
            casas_possiveis: list[Casa] = []
            casas_nao_possiveis = []

            tam_linha = len(tabuleiro)
            tam_coluna = len(tabuleiro[0])
            linha = 0
            coluna = 0
            while (linha < tam_linha):
                while (coluna < tam_coluna):
                    if (tabuleiro[linha][coluna].peca != None and tabuleiro[linha][coluna].peca.tonalidade != self.tonalidade):
                        casas_nao_possiveis.extend(tabuleiro[linha][coluna].peca.get_casas_possiveis(tabuleiro))
                    coluna += 1
                linha += 1

            if (i - 1 >= 0):
                if (tabuleiro[i - 1][j].peca is None):
                    casas_possiveis.append(tabuleiro[i - 1][j])
                elif (self.tonalidade != tabuleiro[i - 1][j].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i - 1][j])   

            if (i + 1 < 8):
                if (tabuleiro[i + 1][j].peca is None):
                    casas_possiveis.append(tabuleiro[i + 1][j])
                elif (self.tonalidade != tabuleiro[i + 1][j].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i + 1][j])

            if (j - 1 >= 0):
                if (tabuleiro[i][j - 1].peca is None):
                    casas_possiveis.append(tabuleiro[i][j - 1])
                elif (self.tonalidade != tabuleiro[i][j - 1].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i][j - 1])

            if (j + 1 < 8):
                if (tabuleiro[i][j + 1].peca is None):
                    casas_possiveis.append(tabuleiro[i][j + 1])
                elif (self.tonalidade != tabuleiro[i][j + 1].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i][j + 1])

            if (i - 1 >= 0 and j - 1 >= 0):
                if (tabuleiro[i - 1][j - 1].peca is None):
                    casas_possiveis.append(tabuleiro[i - 1][j - 1])
                elif (self.tonalidade != tabuleiro[i - 1][j - 1].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i - 1][j - 1])

            if (i - 1 >= 0 and j + 1 < 8):
                if (tabuleiro[i - 1][j + 1].peca is None):
                    casas_possiveis.append(tabuleiro[i - 1][j + 1])
                elif (self.tonalidade != tabuleiro[i - 1][j + 1].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i - 1][j + 1])

            if (i + 1 < 8 and j - 1 >= 0):
                if (tabuleiro[i + 1][j - 1].peca is None):
                    casas_possiveis.append(tabuleiro[i + 1][j - 1])
                elif (self.tonalidade != tabuleiro[i + 1][j - 1].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i + 1][j - 1])

            if (i + 1 < 8 and j + 1 < 8):
                if (tabuleiro[i + 1][j + 1].peca is None):
                    casas_possiveis.append(tabuleiro[i + 1][j + 1])
                elif (self.tonalidade != tabuleiro[i + 1][j + 1].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i + 1][j + 1])  

            
            i = 0
            j = 0
            tam_possiveis = len(casas_possiveis)
            tam_nao_possiveis = len(casas_nao_possiveis)
            while(i < tam_possiveis):
                while(j < tam_nao_possiveis):
                    if (casas_possiveis[i].posicao == casas_nao_possiveis[j].posicao):
                        casas_possiveis.pop(i)
                    j += 1
                i += 1

            return casas_possiveis

        elif (self.tonalidade == 'escuro'):
            casas_possiveis: list[Casa] = []
            casas_nao_possiveis = []

            tam_linha = len(tabuleiro)
            tam_coluna = len(tabuleiro[0])
            linha = 0
            coluna = 0
            while (linha < tam_linha):
                while (coluna < tam_coluna):
                    if (tabuleiro[linha][coluna].peca != None and tabuleiro[linha][coluna].peca.tonalidade != self.tonalidade):
                        casas_nao_possiveis.extend(tabuleiro[linha][coluna].peca.get_casas_possiveis(tabuleiro))
                    coluna += 1
                linha += 1

            if (i - 1 >= 0):
                if (tabuleiro[i - 1][j].peca is None):
                    casas_possiveis.append(tabuleiro[i - 1][j])
                elif (self.tonalidade != tabuleiro[i - 1][j].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i - 1][j])   

            if (i + 1 < 8):
                if (tabuleiro[i + 1][j].peca is None):
                    casas_possiveis.append(tabuleiro[i + 1][j])
                elif (self.tonalidade != tabuleiro[i + 1][j].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i + 1][j])

            if (j - 1 >= 0):
                if (tabuleiro[i][j - 1].peca is None):
                    casas_possiveis.append(tabuleiro[i][j - 1])
                elif (self.tonalidade != tabuleiro[i][j - 1].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i][j - 1])

            if (j + 1 < 8):
                if (tabuleiro[i][j + 1].peca is None):
                    casas_possiveis.append(tabuleiro[i][j + 1])
                elif (self.tonalidade != tabuleiro[i][j + 1].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i][j + 1])

            if (i - 1 >= 0 and j - 1 >= 0):
                if (tabuleiro[i - 1][j - 1].peca is None):
                    casas_possiveis.append(tabuleiro[i - 1][j - 1])
                elif (self.tonalidade != tabuleiro[i - 1][j - 1].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i - 1][j - 1])

            if (i - 1 >= 0 and j + 1 < 8):
                if (tabuleiro[i - 1][j + 1].peca is None):
                    casas_possiveis.append(tabuleiro[i - 1][j + 1])
                elif (self.tonalidade != tabuleiro[i - 1][j + 1].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i - 1][j + 1])

            if (i + 1 < 8 and j - 1 >= 0):
                if (tabuleiro[i + 1][j - 1].peca is None):
                    casas_possiveis.append(tabuleiro[i + 1][j - 1])
                elif (self.tonalidade != tabuleiro[i + 1][j - 1].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i + 1][j - 1])

            if (i + 1 < 8 and j + 1 < 8):
                if (tabuleiro[i + 1][j + 1].peca is None):
                    casas_possiveis.append(tabuleiro[i + 1][j + 1])
                elif (self.tonalidade != tabuleiro[i + 1][j + 1].peca.tonalidade):
                    casas_possiveis.append(tabuleiro[i + 1][j + 1])  

            
            i = 0
            j = 0
            tam_possiveis = len(casas_possiveis)
            tam_nao_possiveis = len(casas_nao_possiveis)
            while(i < tam_possiveis):
                while(j < tam_nao_possiveis):
                    if (casas_possiveis[i].posicao == casas_nao_possiveis[j].posicao):
                        casas_possiveis.pop(i)
                    j += 1
                i += 1

        return casas_possiveis

        
