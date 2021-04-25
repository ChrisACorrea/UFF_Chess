import pygame
from pygame.sprite import Group, AbstractGroup
import time
from casa import Casa
from pecas_models.bispo import Bispo
from pecas_models.pecaBase import PecaBase
from pecas_models.peao import Peao
from pecas_models.rainha import Rainha
from pecas_models.rei import Rei
from pecas_models.torre import Torre
import random

class Tabuleiro(pygame.sprite.Sprite):

    def __init__(self, display: pygame.Surface, *groups: AbstractGroup, jogador1, jogador2):
        super().__init__(*groups)
        self.display: pygame.Surface
        self.objectGroup: Group
        self.vetor_de_Controle: list[list[Casa]] = []
        self.casa_selecionada: Casa = None
        self.casas_possiveis: list[Casa] = []
        self.vez = 'claro'
        self.display = display
        self.altura_tela = display.get_height()
        self.objectGroup = pygame.sprite.Group()

        # variável que guarda a referência dos dois reis para consultas rápidas
        # branco no indice [0] e preto no indice [1]
        self.reis: tuple[Rei, Rei] = [None, None]

        self.iniciar_tabuleiro()

        global jogadorOne
        jogadorOne = jogador1
        global jogadorTwo
        jogadorTwo = jogador2

    def iniciar_tabuleiro(self):
        for i in range(0, 8, 1):
            self.vetor_de_Controle.append([])
            for j in range(0, 8, 1):
                self.vetor_de_Controle[i].append(Casa(self.objectGroup,
                                                      display=self.display,
                                                      posicao_na_matriz=(i, j)))
        self.iniciar_pecas()

    def iniciar_pecas(self):
        for i in range(0, 8, 1):
            for j in range(0, 8, 1):
                self.vetor_de_Controle[i][j].carregar_peca()

                # Guarda a referência dos reis
                if type(self.vetor_de_Controle[i][j].peca) == Rei:
                    if self.vetor_de_Controle[i][j].peca.tonalidade == 'claro':
                        self.reis[0] = self.vetor_de_Controle[i][j].peca
                    else:
                        self.reis[1] = self.vetor_de_Controle[i][j].peca

    def desenhar_tabuleiro(self) -> None:
        self.objectGroup.draw(self.display)
        return

    def clicou_dentro_do_tabuleiro(self, posicao_mouse: tuple[int, int]) -> bool:
        if ((self.vetor_de_Controle[0][0].rect.left < posicao_mouse[0] < self.vetor_de_Controle[7][7].rect.right) and
                (self.vetor_de_Controle[0][0].rect.top < posicao_mouse[1] < self.vetor_de_Controle[7][7].rect.bottom)):
            return True
        return False

    def calcular_casa(self, posicao_mouse: tuple[int, int]):
        tamanho: int = int(self.display.get_height() / 10)
        i: int = int((posicao_mouse[1] - tamanho) / tamanho)
        j: int = int((posicao_mouse[0] - ((self.display.get_width() - (tamanho * 8)) / 2)) / tamanho)
        return [i, j]

    def selecionar_casa(self, posicao_mouse: tuple[int, int], posicao_ia: tuple = None):

        if(posicao_ia is None):
            posicao_casa = self.calcular_casa(posicao_mouse)
            i: int = posicao_casa[0]
            j: int = posicao_casa[1]
        else:
            i: int = posicao_ia[0]
            j: int = posicao_ia[1]

        print('Clicou em', self.vetor_de_Controle[i][j].posicao, self.vetor_de_Controle[i][j].posicao_na_matriz)

        if self.vetor_de_Controle[i][j].possivel:
            print("Movendo peça para casa", self.vetor_de_Controle[i][j].posicao, self.vetor_de_Controle[i][j].posicao_na_matriz)
            self.mover_peca(self.vetor_de_Controle[i][j])
            self.limpar_selecoes()

        elif self.vetor_de_Controle[i][j].peca:
            print("Peça nessa casa: ", self.vetor_de_Controle[i][j].peca.id)
            self.limpar_selecoes()
            if self.vetor_de_Controle[i][j].peca.tonalidade == self.vez:
                self.casa_selecionada = self.vetor_de_Controle[i][j]
                self.casa_selecionada.marcar_como_selecionado()
                print('Casa selecionada', self.casa_selecionada.posicao, self.casa_selecionada.selecionado)
                self.marcar_casas_possiveis()

        else:
            self.limpar_selecoes()

    def marcar_casas_possiveis(self):
        posicao_casa_selecionada = self.casa_selecionada.posicao_na_matriz
        i: int = posicao_casa_selecionada[0]
        j: int = posicao_casa_selecionada[1]

        self.casas_possiveis = self.vetor_de_Controle[i][j].peca.get_casas_possiveis(self.vetor_de_Controle)

        # Não permite que uma peça saia do lugar e deixe seu rei em xeque
        casas_xeque_tratadas = self.tratar_possivel_xeque(self.vetor_de_Controle[i][j].peca, self.casas_possiveis)
        if casas_xeque_tratadas is not None:
            self.casas_possiveis.clear()
            self.casas_possiveis.extend(casas_xeque_tratadas)

        if self.rei_em_xeque() and type(self.vetor_de_Controle[i][j].peca) != Rei:
            # Deixa como casas possíveis somente aquelas entre o rei e o ameaçante (incluindo o ameaçante)
            self.casas_possiveis = self.tratar_casas_possiveis(self.casas_possiveis)

        for i in range(0, len(self.casas_possiveis), 1):
            self.casas_possiveis[i].marcar_como_possivel()

    def limpar_selecoes(self):
        if self.casa_selecionada:
            self.casa_selecionada.desmarcar_como_selecionado()

        self.casa_selecionada = None

        for i in range(0, len(self.casas_possiveis), 1):
            self.casas_possiveis[i].desmarcar_como_possivel()
            self.casas_possiveis[i].is_roque = False
            self.casas_possiveis[i].is_en_passant = False

        self.casas_possiveis.clear()

    def mover_peca(self, casa_destino: Casa):
        peca_movida: PecaBase = self.casa_selecionada.peca
        peca_movida.movimentos += 1
        self.casa_selecionada.remover_peca()

        if casa_destino.is_roque:
            casa_destino.inserir_peca(peca_movida)
            i = casa_destino.posicao_na_matriz[0]

            if casa_destino.posicao_na_matriz[1] > 4:
                torre = self.vetor_de_Controle[i][7].peca
                torre.movimentos += 1
                self.vetor_de_Controle[i][7].remover_peca()
                self.vetor_de_Controle[i][5].inserir_peca(torre)

            if casa_destino.posicao_na_matriz[1] < 4:
                torre = self.vetor_de_Controle[i][0].peca
                torre.movimentos += 1
                self.vetor_de_Controle[i][0].remover_peca()
                self.vetor_de_Controle[i][3].inserir_peca(torre)

        elif casa_destino.is_en_passant:
            casa_destino.inserir_peca(peca_movida)

            i = casa_destino.posicao_na_matriz[0]
            j = casa_destino.posicao_na_matriz[1]

            if casa_destino.peca.tonalidade == 'claro':
                self.vetor_de_Controle[i + 1][j].remover_peca(True)
            else:
                self.vetor_de_Controle[i - 1][j].remover_peca(True)

        else:
            casa_destino.inserir_peca(peca_movida)

        self.promocao()
        self.trocar_vez()
        self.verifica_xeque()
        self.houve_xeque_mate()
        # IA:
        self.melhor_movimento()

    def trocar_vez(self):
        if self.vez == 'claro':
            self.vez = 'escuro'
            self.mostrar_vez(jogadorTwo)
        elif self.vez == 'escuro':
            self.vez = 'claro'
            self.mostrar_vez(jogadorOne)

    def mostrar_vez(self, jogador):
        self.limpar_selecoes();
        self.desenhar_tabuleiro();
        pygame.display.update()
        time.sleep(0.5)
        txt = 'Vez do jogador ' + jogador  ##### armazena o texto
        pygame.font.init()  ##### inicia font
        fonte = pygame.font.get_default_font()  ##### carrega com a fonte padrão
        fontesys = pygame.font.SysFont(fonte, 50)  ##### usa a fonte padrão
        txttela = fontesys.render(txt, 1, (255, 255, 255))  ##### renderiza o texto na cor desejada
        self.display.blit(txttela, (470, 15))  ##### coloca na posição 50,900 (tela FHD)
        pygame.display.update()
        time.sleep(2)

    def promocao(self):
        for i in range(0, 8):
            if type(self.vetor_de_Controle[0][i].peca) == Peao:
                casa: Casa = self.vetor_de_Controle[0][i]
                peca: Peao = self.vetor_de_Controle[0][i].peca
                rainha = Rainha(peca.groups(), rect_base=casa.rect, tom=peca.tonalidade, posicao=peca.posicao,casaOrigem=peca.id)
                self.vetor_de_Controle[0][i].inserir_peca(rainha)
            if type(self.vetor_de_Controle[7][i].peca) == Peao:
                casa: Casa = self.vetor_de_Controle[0][i]
                peca: Peao = self.vetor_de_Controle[7][i].peca
                rainha = Rainha(peca.groups(), rect_base=casa.rect, tom=peca.tonalidade, posicao=peca.posicao,casaOrigem=peca.id)
                self.vetor_de_Controle[7][i].inserir_peca(rainha)

    def verifica_xeque(self):
        self.get_rei_da_vez().limpar_ameacantes()

        for i in range(0, 8):
            for j in range(0, 8):
                casa: Casa = self.vetor_de_Controle[i][j]
                if casa.peca is not None:
                    if casa.peca.tonalidade != self.vez:
                        casa_possiveis = casa.peca.get_casas_possiveis(self.vetor_de_Controle)
                        for k in range(0, len(casa_possiveis)):
                            if type(casa_possiveis[k].peca) == Rei:
                                casa_possiveis[k].peca.add_ameacante(casa.peca)

    def get_rei_da_vez(self) -> Rei:
        return self.reis[0] if self.vez == 'claro' else self.reis[1]

    def rei_em_xeque(self) -> bool:
        return self.get_rei_da_vez().is_xeque()

    def tratar_casas_possiveis(self, casas_possiveis: list[Casa]):
        rei_da_vez: Rei = self.get_rei_da_vez()
        posicao_rei = rei_da_vez.posicao
        ameacantes: list[PecaBase] = rei_da_vez.ameacantes
        casas_de_salvamento: list[Casa] = []
        casas_de_defesa: list[Casa] = []

        for i in range(0, len(ameacantes)):
            posicao_ameacante = ameacantes[i].posicao
            casas_de_salvamento.append(self.vetor_de_Controle[posicao_ameacante[0]][posicao_ameacante[1]])

            if posicao_rei[0] == posicao_ameacante[0]:
                step = 1 if posicao_ameacante[1] > posicao_rei[1] else -1
                for coluna in range(posicao_rei[1] + step, posicao_ameacante[1]):
                    casas_de_salvamento.append(self.vetor_de_Controle[posicao_rei[0]][coluna])
            elif posicao_rei[1] == posicao_ameacante[1]:
                step = 1 if posicao_ameacante[0] > posicao_rei[0] else -1
                for linha in range(posicao_rei[0] + step, posicao_ameacante[0]):
                    casas_de_salvamento.append(self.vetor_de_Controle[linha][posicao_rei[1]])
            else:
                if type(ameacantes[i]) == Bispo or type(ameacantes[i]) == Rainha:
                    step_l = 1 if posicao_ameacante[0] > posicao_rei[0] else -1
                    step_c = 1 if posicao_ameacante[1] > posicao_rei[1] else -1
                    linha = posicao_rei[0] + step_l
                    coluna = posicao_rei[1] + step_c
                    while posicao_ameacante[0] != linha and posicao_ameacante[1] != coluna:
                        casas_de_salvamento.append(self.vetor_de_Controle[linha][coluna])
                        linha += step_l
                        coluna += step_c

        for i in range(0, len(casas_possiveis)):
            for j in range(0, len(casas_de_salvamento)):
                if casas_possiveis[i].posicao == casas_de_salvamento[j].posicao:
                    casas_de_defesa.append(casas_de_salvamento[j])

        return casas_de_defesa

    def tratar_possivel_xeque(self, peca_selecionada: PecaBase, casas_possiveis: list[Casa]):
        posicao_peca = peca_selecionada.posicao
        caminho_da_salvacao: list[Casa] = []
        caminho_da_morte = self.get_caminho_da_morte(posicao_peca)

        if len(caminho_da_morte) != 0:
            for i in range(0, len(casas_possiveis)):
                for j in range(0, len(caminho_da_morte)):
                    if casas_possiveis[i].posicao == caminho_da_morte[j].posicao:
                        caminho_da_salvacao.append(caminho_da_morte[j])

            return caminho_da_salvacao

        return None

    def get_casas_superior(self, posicao_atual: tuple[int, int]):
        casas_encontradas: list[Casa] = []
        i = posicao_atual[0]
        j = posicao_atual[1]

        while i >= 1:
            i -= 1
            if self.vetor_de_Controle[i][j].peca is None:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
            else:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
                break

        return casas_encontradas

    def get_casas_inferior(self, posicao_atual: tuple[int, int]):
        casas_encontradas: list[Casa] = []
        i = posicao_atual[0]
        j = posicao_atual[1]

        while i < 7:
            i += 1
            if self.vetor_de_Controle[i][j].peca is None:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
            else:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
                break

        return casas_encontradas

    def get_casas_direita(self, posicao_atual: tuple[int, int]):
        casas_encontradas: list[Casa] = []
        i = posicao_atual[0]
        j = posicao_atual[1]

        while j < 7:
            j += 1
            if self.vetor_de_Controle[i][j].peca is None:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
            else:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
                break

        return casas_encontradas

    def get_casas_esquerda(self, posicao_atual: tuple[int, int]):
        casas_encontradas: list[Casa] = []
        i = posicao_atual[0]
        j = posicao_atual[1]

        while j >= 1:
            j -= 1
            if self.vetor_de_Controle[i][j].peca is None:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
            else:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
                break

        return casas_encontradas

    def get_casas_diagonal_superior_direita(self, posicao_atual: tuple[int, int]):
        casas_encontradas: list[Casa] = []
        i = posicao_atual[0]
        j = posicao_atual[1]

        while i >= 1 and j < 7:
            i -= 1
            j += 1
            if self.vetor_de_Controle[i][j].peca is None:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
            else:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
                break

        return casas_encontradas

    def get_casas_diagonal_inferior_direita(self, posicao_atual: tuple[int, int]):
        casas_encontradas: list[Casa] = []
        i = posicao_atual[0]
        j = posicao_atual[1]

        while i < 7 and j < 7:
            i += 1
            j += 1
            if self.vetor_de_Controle[i][j].peca is None:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
            else:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
                break

        return casas_encontradas

    def get_casas_diagonal_inferior_esquerda(self, posicao_atual: tuple[int, int]):
        casas_encontradas: list[Casa] = []
        i = posicao_atual[0]
        j = posicao_atual[1]

        while i < 7 and j >= 1:
            i += 1
            j -= 1
            if self.vetor_de_Controle[i][j].peca is None:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
            else:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
                break

        return casas_encontradas

    def get_casas_diagonal_superior_esquerda(self, posicao_atual: tuple[int, int]):
        casas_encontradas: list[Casa] = []
        i = posicao_atual[0]
        j = posicao_atual[1]

        while i >= 1 and j >= 1:
            i -= 1
            j -= 1
            if self.vetor_de_Controle[i][j].peca is None:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
            else:
                casas_encontradas.append(self.vetor_de_Controle[i][j])
                break

        return casas_encontradas

    def get_caminho_da_morte(self, posicao_peca):
        caminho_da_morte: list[Casa] = []

        direcao_rei = self.get_casas_superior(posicao_peca)
        if len(direcao_rei) != 0:
            if type(direcao_rei[-1].peca) == Rei and direcao_rei[-1].peca.tonalidade == self.vez:
                direcao_contraria = self.get_casas_inferior(posicao_peca)
                if len(direcao_contraria) != 0:
                    if direcao_contraria[-1].peca is not None:
                        if direcao_contraria[-1].peca.tonalidade != self.vez:
                            if type(direcao_contraria[-1].peca) == Rainha or type(direcao_contraria[-1].peca) == Torre:
                                caminho_da_morte.extend(direcao_contraria)
                                caminho_da_morte.extend(direcao_rei)
                                return caminho_da_morte
                    else:
                        return caminho_da_morte

        direcao_rei = self.get_casas_inferior(posicao_peca)
        if len(direcao_rei) != 0:
            if type(direcao_rei[-1].peca) == Rei and direcao_rei[-1].peca.tonalidade == self.vez:
                direcao_contraria = self.get_casas_superior(posicao_peca)
                if len(direcao_contraria) != 0:
                    if direcao_contraria[-1].peca is not None:
                        if direcao_contraria[-1].peca.tonalidade != self.vez:
                            if type(direcao_contraria[-1].peca) == Rainha or type(direcao_contraria[-1].peca) == Torre:
                                caminho_da_morte.extend(direcao_contraria)
                                caminho_da_morte.extend(direcao_rei)
                                return caminho_da_morte
                    else:
                        return caminho_da_morte

        direcao_rei = self.get_casas_direita(posicao_peca)
        if len(direcao_rei) != 0:
            if type(direcao_rei[-1].peca) == Rei and direcao_rei[-1].peca.tonalidade == self.vez:
                direcao_contraria = self.get_casas_esquerda(posicao_peca)
                if len(direcao_contraria) != 0:
                    if direcao_contraria[-1].peca is not None:
                        if direcao_contraria[-1].peca.tonalidade != self.vez:
                            if type(direcao_contraria[-1].peca) == Rainha or type(direcao_contraria[-1].peca) == Torre:
                                caminho_da_morte.extend(direcao_contraria)
                                caminho_da_morte.extend(direcao_rei)
                                return caminho_da_morte
                    else:
                        return caminho_da_morte

        direcao_rei = self.get_casas_esquerda(posicao_peca)
        if len(direcao_rei) != 0:
            if type(direcao_rei[-1].peca) == Rei and direcao_rei[-1].peca.tonalidade == self.vez:
                direcao_contraria = self.get_casas_direita(posicao_peca)
                if len(direcao_contraria) != 0:
                    if direcao_contraria[-1].peca is not None:
                        if direcao_contraria[-1].peca.tonalidade != self.vez:
                            if type(direcao_contraria[-1].peca) == Rainha or type(direcao_contraria[-1].peca) == Torre:
                                caminho_da_morte.extend(direcao_contraria)
                                caminho_da_morte.extend(direcao_rei)
                                return caminho_da_morte
                    else:
                        return caminho_da_morte

        direcao_rei = self.get_casas_diagonal_superior_direita(posicao_peca)
        if len(direcao_rei) != 0:
            if type(direcao_rei[-1].peca) == Rei and direcao_rei[-1].peca.tonalidade == self.vez:
                direcao_contraria = self.get_casas_diagonal_inferior_esquerda(posicao_peca)
                if len(direcao_contraria) != 0:
                    if direcao_contraria[-1].peca is not None:
                        if direcao_contraria[-1].peca.tonalidade != self.vez:
                            if type(direcao_contraria[-1].peca) == Rainha or type(direcao_contraria[-1].peca) == Bispo:
                                caminho_da_morte.extend(direcao_contraria)
                                caminho_da_morte.extend(direcao_rei)
                                return caminho_da_morte
                    else:
                        return caminho_da_morte

        direcao_rei = self.get_casas_diagonal_inferior_esquerda(posicao_peca)
        if len(direcao_rei) != 0:
            if type(direcao_rei[-1].peca) == Rei and direcao_rei[-1].peca.tonalidade == self.vez:
                direcao_contraria = self.get_casas_diagonal_superior_direita(posicao_peca)
                if len(direcao_contraria) != 0:
                    if direcao_contraria[-1].peca is not None:
                        if direcao_contraria[-1].peca.tonalidade != self.vez:
                            if type(direcao_contraria[-1].peca) == Rainha or type(direcao_contraria[-1].peca) == Bispo:
                                caminho_da_morte.extend(direcao_contraria)
                                caminho_da_morte.extend(direcao_rei)
                                return caminho_da_morte
                    else:
                        return caminho_da_morte

        direcao_rei = self.get_casas_diagonal_inferior_direita(posicao_peca)
        if len(direcao_rei) != 0:
            if type(direcao_rei[-1].peca) == Rei and direcao_rei[-1].peca.tonalidade == self.vez:
                direcao_contraria = self.get_casas_diagonal_superior_esquerda(posicao_peca)
                if len(direcao_contraria) != 0:
                    if direcao_contraria[-1].peca is not None:
                        if direcao_contraria[-1].peca.tonalidade != self.vez:
                            if type(direcao_contraria[-1].peca) == Rainha or type(direcao_contraria[-1].peca) == Bispo:
                                caminho_da_morte.extend(direcao_contraria)
                                caminho_da_morte.extend(direcao_rei)
                                return caminho_da_morte
                    else:
                        return caminho_da_morte

        direcao_rei = self.get_casas_diagonal_superior_esquerda(posicao_peca)
        if len(direcao_rei) != 0:
            if type(direcao_rei[-1].peca) == Rei and direcao_rei[-1].peca.tonalidade == self.vez:
                direcao_contraria = self.get_casas_diagonal_inferior_direita(posicao_peca)
                if len(direcao_contraria) != 0:
                    if direcao_contraria[-1].peca is not None:
                        if direcao_contraria[-1].peca.tonalidade != self.vez:
                            if type(direcao_contraria[-1].peca) == Rainha or type(direcao_contraria[-1].peca) == Bispo:
                                caminho_da_morte.extend(direcao_contraria)
                                caminho_da_morte.extend(direcao_rei)
                                return caminho_da_morte
                    else:
                        return caminho_da_morte

        return caminho_da_morte

    def houve_xeque_mate(self):
        todas_casas_possiveis: list[Casa] = []

        for i in range(8):
            for j in range(8):
                if self.vetor_de_Controle[i][j].peca is not None:
                    peca = self.vetor_de_Controle[i][j].peca
                    if peca.tonalidade == self.vez:
                        casas_possiveis_peca = peca.get_casas_possiveis(self.vetor_de_Controle)
                        casas_possivel_cheque_tratadas = self.tratar_possivel_xeque(peca, casas_possiveis_peca)
                        if casas_possivel_cheque_tratadas is not None:
                            todas_casas_possiveis.extend(casas_possivel_cheque_tratadas)
                        todas_casas_possiveis = self.tratar_casas_possiveis(todas_casas_possiveis)

        if len(todas_casas_possiveis) == 0 and self.get_rei_da_vez().is_xeque():
            self.mostrar_msg_xeque_mate()
            print("XEQUE MATE SEU OTÁRIO")

    def mostrar_msg_xeque_mate(self):
        txt = 'XEQUE-MATE'  ##### armazena o texto
        pygame.font.init()  ##### inicia font
        fonte = pygame.font.get_default_font()  ##### carrega com a fonte padrão
        fontesys = pygame.font.SysFont(fonte, 200)  ##### usa a fonte padrão
        txttela = fontesys.render(txt, 1, (255, 255, 255), (0, 0, 0))  ##### renderiza o texto na cor desejada
        self.display.blit(txttela, ((self.display.get_width() / 2) - (txttela.get_width() / 2), (self.display.get_height() / 2) - (txttela.get_height() / 2)))  ##### coloca na posição 50,900 (tela FHD)
        pygame.display.update()
        time.sleep(10)

    def calcular_placar(self):
        placar = 0
        for i in range(8):
            for j in range(8):
                if self.vetor_de_Controle[i][j].peca is not None:
                    peca = self.vetor_de_Controle[i][j].peca
                    placar +=  peca.valor
        print("PLACAR:", placar)

    def melhor_movimento(self):
        if self.vez == "claro":
            return
        placar = self.calcular_placar()
        maior = 0
        casa_destino = None
        casa_origem = None
        jogadas_aleatorias_possiveis = []
        vetor_de_controle_inicial = self.vetor_de_Controle

        # e

        # selecionar jogada que captura a melhor peça, se houver, ou adicionar as jogadas possíveis a um vetor
        for i in range(8):
            for j in range(8):
                if self.vetor_de_Controle[i][j].peca is not None:
                    peca = self.vetor_de_Controle[i][j].peca
                    if peca.tonalidade == self.vez:
                        for casa in peca.get_casas_possiveis(self.vetor_de_Controle):
                            # tentando selecionar jogada que captura a melhor peça, se houver
                            if casa.peca is not None and casa.peca.tonalidade == "claro":
                                if (casa.peca.valor >= maior):
                                    maior = casa.peca.valor
                                    casa_destino = casa
                                    casa_origem = self.vetor_de_Controle[i][j]
                        if peca is not None and len(peca.get_casas_possiveis(self.vetor_de_Controle)) > 0:
                            # ATENÇÃO: verificar se ele está sabendo quem é a peça que está sendo movida
                            jogadas_aleatorias_possiveis.append(self.vetor_de_Controle[i][j])


        if casa_destino is None:
            tam_origem = len(jogadas_aleatorias_possiveis)
            index = random.randrange(0, tam_origem, 1)
            casa_origem = jogadas_aleatorias_possiveis[index]
            casa_origem.marcar_como_selecionado()

            tam_destino = len(casa_origem.peca.get_casas_possiveis(self.vetor_de_Controle))
            index_destino = random.randrange(0, tam_destino, 1)
            casa_destino = casa_origem.peca.get_casas_possiveis(self.vetor_de_Controle)[index_destino]
            casa_destino.marcar_como_possivel()
            self.casa_selecionada = casa_origem
            self.selecionar_casa(casa_destino, casa_destino.posicao_na_matriz)
            # casa_destino.desmarcar_como_selecionado()
            self.limpar_selecoes()

        else:
            casa_destino.marcar_como_possivel()
            self.casa_selecionada = casa_origem
            self.selecionar_casa(casa_destino, casa_destino.posicao_na_matriz)
            # casa_destino.desmarcar_como_selecionado()
            # self.mover_peca(casa_destino)
            self.limpar_selecoes()



    # IA versus IA
    # def melhor_movimento(self):
    #     placar = self.calcular_placar()
    #     posicao = None
    #     vetor_de_controle_inicial = self.vetor_de_Controle
    #     for i in range(8):
    #         for j in range(8):
    #             if self.vetor_de_Controle[i][j].peca is not None:
    #                 peca = self.vetor_de_Controle[i][j].peca
    #                 if peca.tonalidade == self.vez:
    #                     #(APAGAR) ideia: usar um vetor de controle falso
    #                     for casa in peca.get_casas_possiveis(self.vetor_de_Controle):
    #                         self.selecionar_casa(casa, [i,j])
    #                         self.mover_peca(casa)
    #                         # self.vetor_de_Controle = vetor_de_controle_inicial
    #
    #                     placar_temp = self.calcular_placar()
    #                     # para as claras o placar deve ser o maior possível
    #                     if placar_temp is not None and placar is not None and placar_temp > placar:
    #                         placar = placar_temp
    #                         #por enquanto salvando apenas a posicao da peça
    #                         posicao = peca.posicao
