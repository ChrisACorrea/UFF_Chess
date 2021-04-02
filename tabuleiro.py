import pygame
from pygame.sprite import Group, AbstractGroup
import time
from casa import Casa
from pecas_models.bispo import Bispo
from pecas_models.pecaBase import PecaBase
from pecas_models.peao import Peao
from pecas_models.rainha import Rainha
from pecas_models.rei import Rei


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

    def selecionar_casa(self, posicao_mouse: tuple[int, int]):
        posicao_casa = self.calcular_casa(posicao_mouse)
        i: int = posicao_casa[0]
        j: int = posicao_casa[1]
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

        if self.rei_em_xeque() and type(self.vetor_de_Controle[i][j].peca) != Rei:
            self.tratar_casas_possiveis()

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

    def trocar_vez(self):
        if self.vez == 'claro':
            self.vez = 'escuro'
            #self.mostrar_vez(jogadorTwo)
        elif self.vez == 'escuro':
            self.vez = 'claro'
            #self.mostrar_vez(jogadorOne)

    def mostrar_vez(self, jogador):
        txt = 'Vez do jogador ' + jogador  ##### armazena o texto
        pygame.font.init()  ##### inicia font
        fonte = pygame.font.get_default_font()  ##### carrega com a fonte padrão
        fontesys = pygame.font.SysFont(fonte, 120)  ##### usa a fonte padrão
        txttela = fontesys.render(txt, 1, (255, 255, 255))  ##### renderiza o texto na cor desejada
        self.display.blit(txttela, (270, 320))  ##### coloca na posição 50,900 (tela FHD)
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

    def tratar_casas_possiveis(self):
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

        for i in range(0, len(self.casas_possiveis)):
            for j in range(0, len(casas_de_salvamento)):
                if self.casas_possiveis[i].posicao == casas_de_salvamento[j].posicao:
                    casas_de_defesa.append(casas_de_salvamento[j])

        self.casas_possiveis.clear()
        self.casas_possiveis.extend(casas_de_defesa)
