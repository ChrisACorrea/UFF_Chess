import pygame
from pygame.sprite import Group, AbstractGroup
import time
from casa import Casa
from pecas_models.pecaBase import PecaBase


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

        for i in range(0, len(self.casas_possiveis), 1):
            self.casas_possiveis[i].marcar_como_possivel()

    def limpar_selecoes(self):
        if self.casa_selecionada:
            self.casa_selecionada.desmarcar_como_selecionado()

        self.casa_selecionada = None

        for i in range(0, len(self.casas_possiveis), 1):
            self.casas_possiveis[i].desmarcar_como_possivel()

        self.casas_possiveis.clear()

    def mover_peca(self, casa_destino: Casa):
        peca_movida: PecaBase = self.casa_selecionada.peca
        peca_movida.movimentos += 1
        self.casa_selecionada.remover_peca()
        casa_destino.inserir_peca(peca_movida)
        self.trocar_vez()

    def trocar_vez(self):
        if self.vez == 'claro':
            self.vez = 'escuro'
            self.mostrar_vez(jogadorTwo)
        elif self.vez == 'escuro':
            self.vez = 'claro'
            self.mostrar_vez(jogadorOne)

    def mostrar_vez(self, jogador):
        txt = 'Vez do jogador ' + jogador  ##### armazena o texto
        pygame.font.init()  ##### inicia font
        fonte = pygame.font.get_default_font()  ##### carrega com a fonte padrão
        fontesys = pygame.font.SysFont(fonte, 120)  ##### usa a fonte padrão
        txttela = fontesys.render(txt, 1, (255, 255, 255))  ##### renderiza o texto na cor desejada
        self.display.blit(txttela, (270, 320))  ##### coloca na posição 50,900 (tela FHD)
        pygame.display.update()
        time.sleep(2)
