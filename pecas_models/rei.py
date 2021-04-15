from __future__ import annotations

import pygame
from pygame.sprite import AbstractGroup

from appConstants import ImagesPath
#from casa import Casa
from pecas_models.pecaBase import PecaBase
from pecas_models.peao import Peao

class Rei(PecaBase):

    def __init__(self, *groups: AbstractGroup, rect_base: pygame.Rect, tom: str, posicao: tuple[int, int], casaOrigem: str):
        super().__init__(*groups, rect_base=rect_base, tom=tom, posicao=posicao, casaOrigem=casaOrigem)
        self.conta_xeque: int = 0
        if self.tonalidade == 'escuro':
            self.caminho_imagem = ImagesPath.REI_PRETO
        elif self.tonalidade == 'claro':
            self.caminho_imagem = ImagesPath.REI_BRANCO

        # Array de deverá guardar todas as peças que ameaçam o Rei em uma jogada.
        self.ameacantes: list[PecaBase] = []

        self.carregar_imagem(self.rect.copy())

    def carregar_imagem(self, rect_base: pygame.Rect) -> None:
        self.image = pygame.image.load(self.caminho_imagem)
        self.image = pygame.transform.smoothscale(self.image, [self.rect.width, self.rect.height])

    def get_casas_possiveis_sem_tratamento(self, tabuleiro: list[list[Casa]], incluir_casas_ameacadas=False) -> list[Casa]:
        """
        Função exclusiva do Rei.
        Pega todas as casas nas quais a Rei pode ser jogado, porém ser fazer verificação se a casa está sendo ameaçada.

        :param tabuleiro:
        :param incluir_casas_ameacadas:
        :return:
        """

        i: int = self.posicao[0]
        j: int = self.posicao[1]

        casas_possiveis: list[Casa] = []

        if (i - 1 >= 0):
            if (tabuleiro[i - 1][j].peca is None):
                casas_possiveis.append(tabuleiro[i - 1][j])
            elif (self.tonalidade != tabuleiro[i - 1][j].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i - 1][j])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i - 1][j])

        if (i + 1 < 8):
            if (tabuleiro[i + 1][j].peca is None):
                casas_possiveis.append(tabuleiro[i + 1][j])
            elif (self.tonalidade != tabuleiro[i + 1][j].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i + 1][j])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i + 1][j])

        if (j - 1 >= 0):
            if (tabuleiro[i][j - 1].peca is None):
                casas_possiveis.append(tabuleiro[i][j - 1])
            elif (self.tonalidade != tabuleiro[i][j - 1].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i][j - 1])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i][j - 1])

        if (j + 1 < 8):
            if (tabuleiro[i][j + 1].peca is None):
                casas_possiveis.append(tabuleiro[i][j + 1])
            elif (self.tonalidade != tabuleiro[i][j + 1].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i][j + 1])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i][j + 1])

        if (i - 1 >= 0 and j - 1 >= 0):
            if (tabuleiro[i - 1][j - 1].peca is None):
                casas_possiveis.append(tabuleiro[i - 1][j - 1])
            elif (self.tonalidade != tabuleiro[i - 1][j - 1].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i - 1][j - 1])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i - 1][j - 1])

        if (i - 1 >= 0 and j + 1 < 8):
            if (tabuleiro[i - 1][j + 1].peca is None):
                casas_possiveis.append(tabuleiro[i - 1][j + 1])
            elif (self.tonalidade != tabuleiro[i - 1][j + 1].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i - 1][j + 1])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i - 1][j + 1])

        if (i + 1 < 8 and j - 1 >= 0):
            if (tabuleiro[i + 1][j - 1].peca is None):
                casas_possiveis.append(tabuleiro[i + 1][j - 1])
            elif (self.tonalidade != tabuleiro[i + 1][j - 1].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i + 1][j - 1])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i + 1][j - 1])

        if (i + 1 < 8 and j + 1 < 8):
            if (tabuleiro[i + 1][j + 1].peca is None):
                casas_possiveis.append(tabuleiro[i + 1][j + 1])
            elif (self.tonalidade != tabuleiro[i + 1][j + 1].peca.tonalidade):
                casas_possiveis.append(tabuleiro[i + 1][j + 1])
            elif incluir_casas_ameacadas:
                casas_possiveis.append(tabuleiro[i + 1][j + 1])

        return casas_possiveis

    def get_casas_possiveis(self, tabuleiro: list[list[Casa]], incluir_casas_ameacadas=False) -> list[Casa]:

        casas_possiveis_sem_tratamento: list[Casa] = self.get_casas_possiveis_sem_tratamento(tabuleiro)
        casas_possiveis: list[Casa] = []
        casas_nao_possiveis: list[Casa] = []

        tam_linha = len(tabuleiro)
        tam_coluna = len(tabuleiro[0])
        linha = 0
        coluna = 0
        while (linha < tam_linha):
            while (coluna < tam_coluna):
                if (tabuleiro[linha][coluna].peca != None):
                    if tabuleiro[linha][coluna].peca.tonalidade != self.tonalidade:
                        casas_ameacadas: list[Casa]

                        if type(tabuleiro[linha][coluna].peca) == Rei:
                            casas_ameacadas = tabuleiro[linha][coluna].peca.get_casas_possiveis_sem_tratamento(tabuleiro, True)
                        elif type(tabuleiro[linha][coluna].peca) == Peao:
                            casas_ameacadas = tabuleiro[linha][coluna].peca.get_casas_de_captura(tabuleiro)
                        else:
                            casas_ameacadas = tabuleiro[linha][coluna].peca.get_casas_possiveis(tabuleiro, True)

                        # Se o Rei estiver em xeque, verifica a posição do ameaçante e não permite que o Rei ande
                        # na direção oposta.
                        if len(self.ameacantes) > 0:
                            for i in range(len(self.ameacantes)):
                                if type(self.ameacantes[i]) != Rei or type(self.ameacantes[i]) != Peao:

                                    # Rei está na mesma linha que ameaçante?
                                    if self.posicao[0] == self.ameacantes[i].posicao[0]:
                                        if(self.posicao[1] > self.ameacantes[i].posicao[1]) and (self.posicao[1] < 7):
                                            casas_ameacadas.append(tabuleiro[self.posicao[0]][self.posicao[1] + 1])
                                        elif (self.posicao[1] < self.ameacantes[i].posicao[1]) and (self.posicao[1] > 0):
                                            casas_ameacadas.append(tabuleiro[self.posicao[0]][self.posicao[1] - 1])

                                    # Rei está na mesma coluna que ameaçante?
                                    elif self.posicao[1] == self.ameacantes[i].posicao[1]:
                                        if(self.posicao[0] > self.ameacantes[i].posicao[0]) and (self.posicao[0] < 7):
                                            casas_ameacadas.append(tabuleiro[self.posicao[0] + 1][self.posicao[1]])
                                        elif (self.posicao[0] < self.ameacantes[i].posicao[0]) and (self.posicao[0] > 0):
                                            casas_ameacadas.append(tabuleiro[self.posicao[0] - 1][self.posicao[1]])

                                    # Então, ameaçante está na diagonal do Rei.
                                    else: 
                                        # Verifica ameaçante no casa superior direita
                                        if((self.posicao[0] > self.ameacantes[i].posicao[0]) and
                                                (self.posicao[1] < self.ameacantes[i].posicao[1])):
                                            # Verifica casa no canto inferior esquerdo
                                            if (self.posicao[0] < 7) and (self.posicao[1] > 0):
                                                casas_ameacadas.append(tabuleiro[self.posicao[0] + 1][self.posicao[1] - 1])
                                        # Verifica ameaçante no casa inferior direita
                                        if ((self.posicao[0] < self.ameacantes[i].posicao[0]) and
                                                (self.posicao[1] < self.ameacantes[i].posicao[1])):
                                            if (self.posicao[0] > 0) and (self.posicao[1] > 0):
                                                casas_ameacadas.append(tabuleiro[self.posicao[0] - 1][self.posicao[1] - 1])
                                        # Verifica ameaçante no casa inferior esquerdo
                                        if ((self.posicao[0] < self.ameacantes[i].posicao[0]) and
                                                (self.posicao[1] > self.ameacantes[i].posicao[1])):
                                            if (self.posicao[0] > 0) and (self.posicao[1] < 7):
                                                casas_ameacadas.append(tabuleiro[self.posicao[0] - 1][self.posicao[1] + 1])
                                        # Verifica ameaçante no casa superior esquerdo
                                        if ((self.posicao[0] > self.ameacantes[i].posicao[0]) and
                                                (self.posicao[1] > self.ameacantes[i].posicao[1])):
                                            if (self.posicao[0] < 7) and (self.posicao[1] < 7):
                                                casas_ameacadas.append(tabuleiro[self.posicao[0] + 1][self.posicao[1] + 1])

                        if len(casas_nao_possiveis) == 0:
                            casas_nao_possiveis.extend(casas_ameacadas)
                        else:
                            for i in range(0, len(casas_ameacadas)):
                                tem_igual = False
                                for j in range(0, len(casas_nao_possiveis)):
                                    if casas_ameacadas[i].posicao == casas_nao_possiveis[j].posicao:
                                        tem_igual = True
                                if not tem_igual:
                                    casas_nao_possiveis.append(casas_ameacadas[i])

                coluna += 1
            linha += 1
            coluna = 0

            # Verifica movimentos do roque
            if self.movimentos == 0 and self.conta_xeque < 1:
                # Verifica lado direito
                if tabuleiro[self.posicao[0]][7].peca is not None:
                    if tabuleiro[self.posicao[0]][7].peca.movimentos == 0:
                        if (tabuleiro[self.posicao[0]][5].peca is None and
                                tabuleiro[self.posicao[0]][6].peca is None):
                            casa_roque_d: Casa = tabuleiro[self.posicao[0]][6]
                            casa_roque_d.is_roque = True
                            casas_possiveis_sem_tratamento.append(casa_roque_d)

                # Verifica lado esquerdo
                if tabuleiro[self.posicao[0]][0].peca is not None:
                    if tabuleiro[self.posicao[0]][0].peca.movimentos == 0:
                        if (tabuleiro[self.posicao[0]][1].peca is None and
                                tabuleiro[self.posicao[0]][2].peca is None and
                                tabuleiro[self.posicao[0]][3].peca is None):
                            casa_roque_e: Casa = tabuleiro[self.posicao[0]][2]
                            casa_roque_e.is_roque = True
                            casas_possiveis_sem_tratamento.append(casa_roque_e)

        # -----
        i = 0
        j = 0
        tam_possiveis = len(casas_possiveis_sem_tratamento)
        tam_nao_possiveis = len(casas_nao_possiveis)

        while(i < tam_possiveis):
            tem_igual = False
            while(j < tam_nao_possiveis):
                if (casas_possiveis_sem_tratamento[i].posicao == casas_nao_possiveis[j].posicao):
                    tem_igual = True
                    casas_possiveis_sem_tratamento[i].is_roque = False
                j += 1
            if not tem_igual:
                casas_possiveis.append(casas_possiveis_sem_tratamento[i])
            i += 1
            j = 0

        return casas_possiveis

    def add_xeque(self):
        self.conta_xeque += 1

    def add_ameacante(self, ameacante: PecaBase):
        self.ameacantes.append(ameacante)
        self.add_xeque()

    def limpar_ameacantes(self):
        self.ameacantes.clear()

    def is_xeque(self):
        return len(self.ameacantes) > 0
