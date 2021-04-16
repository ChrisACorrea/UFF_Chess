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
        """
        Preenche a matriz de controle (vetor_de_controle) com as casas instanciando uma casa para cada posição.
        :return:
        """
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
        """
        Verifica se o clique do mouse aconteceu dentro do tabuleiro.
        :param posicao_mouse:
        :return: True, se clique ocorreu dentro do tabuleiro, senão False
        """
        if ((self.vetor_de_Controle[0][0].rect.left < posicao_mouse[0] < self.vetor_de_Controle[7][7].rect.right) and
                (self.vetor_de_Controle[0][0].rect.top < posicao_mouse[1] < self.vetor_de_Controle[7][7].rect.bottom)):
            return True
        return False

    def calcular_casa(self, posicao_mouse: tuple[int, int]) -> tuple[int, int]:
        """
        Calcula em qual casa o clique aconteceu baseado na posição do mouse.
        :param posicao_mouse:
        :return: Os índices ([linha, coluna]) correspondentes a casa clicada.
        """
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
        """
        Marca no tabuleiro as jogadas possível da atual peça selecionada.

        :return:
        """
        posicao_casa_selecionada = self.casa_selecionada.posicao_na_matriz
        i: int = posicao_casa_selecionada[0]
        j: int = posicao_casa_selecionada[1]

        self.casas_possiveis = self.vetor_de_Controle[i][j].peca.get_casas_possiveis(self.vetor_de_Controle)

        # Não permite que uma peça saia do lugar e deixe seu rei em xeque
        casas_xeque_tratadas = self.tratar_xeque_em_potencial(self.vetor_de_Controle[i][j].peca, self.casas_possiveis)
        if casas_xeque_tratadas is not None:
            self.casas_possiveis.clear()
            self.casas_possiveis.extend(casas_xeque_tratadas)

        if self.rei_em_xeque() and type(self.vetor_de_Controle[i][j].peca) != Rei:
            # Deixa como casas possíveis somente aquelas entre o rei e o ameaçante (incluindo o ameaçante)
            self.casas_possiveis = self.get_casas_que_salvam_o_rei(self.casas_possiveis)

        for i in range(0, len(self.casas_possiveis), 1):
            self.casas_possiveis[i].marcar_como_possivel()

    def limpar_selecoes(self):
        """
        Limpa todas as marcações feitas no tabuleiro.

        :return:
        """
        if self.casa_selecionada:
            self.casa_selecionada.desmarcar_como_selecionado()

        self.casa_selecionada = None

        for i in range(0, len(self.casas_possiveis), 1):
            self.casas_possiveis[i].desmarcar_como_possivel()
            self.casas_possiveis[i].is_roque = False
            self.casas_possiveis[i].is_en_passant = False

        self.casas_possiveis.clear()

    def mover_peca(self, casa_destino: Casa):
        """
        Move a atual peça selecionada para a casa escolhida. Considera jogadas especiais.

        :param casa_destino: Casa que foi escolhida para a peça ser movida.
        :return:
        """
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


    def trocar_vez(self):
        """
        Troca a vez do jogador.

        :return:
        """
        if self.vez == 'claro':
            self.vez = 'escuro'
            self.verifica_xeque()
            status = self.houve_xeque_mate()
            if status == True:
                self.mostrar_msg_xeque_mate(jogadorOne)
            else:
                self.mostrar_vez(jogadorTwo)
        elif self.vez == 'escuro':
            self.vez = 'claro'
            self.verifica_xeque()
            status = self.houve_xeque_mate()
            if status == True:
                self.mostrar_msg_xeque_mate(jogadorTwo)
            else:
                self.mostrar_vez(jogadorOne)

    def mostrar_vez(self, jogador):
        """
        Imprime na tela de qual jogador é a vez.

        :param jogador:
        :return:
        """
        self.limpar_selecoes()
        self.desenhar_tabuleiro()
        pygame.display.update()
        time.sleep(0.5)
        txt = 'Vez do jogador ' + jogador  ##### armazena o texto
        pygame.font.init()  ##### inicia font
        fonte = pygame.font.get_default_font()  ##### carrega com a fonte padrão
        fontesys = pygame.font.SysFont(fonte, 50)  ##### usa a fonte padrão
        txttela = fontesys.render(txt, 1, (255, 255, 255))  ##### renderiza o texto na cor desejada
        self.display.blit(txttela, (480, 15))  ##### coloca na posição 50,900 (tela FHD)
        pygame.display.update()
        time.sleep(1)

    def promocao(self):
        """
        Verifica se um Peão chegou ao fim do tabuleiro e o promove.

        :return:
        """
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
        """
        Varre o tabuleiro e verifica se alguma peça ameaça o Rei, se sim, esta peça é adicionada à lista de ameaçantes
        do Rei ameaçado.
        """
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
        """
        Retorna o Rei do jogador atual.
        """
        return self.reis[0] if self.vez == 'claro' else self.reis[1]

    def rei_em_xeque(self) -> bool:
        """
        Verifica se o Rei do atual jogador está em cheque.

        :return: True se o Rei está em xeque, senão False.
        """
        return self.get_rei_da_vez().is_xeque()

    def get_casas_que_salvam_o_rei(self, casas_possiveis: list[Casa]):
        """
        ATENÇÃO: Está função NÃO deve ser utilizada se Rei NÃO estiver em xeque. E NÃO deve ser utilizada se a peça
        selecionada for um Rei.

        Trata as casas possíveis passadas e deixa somente as casas cuja as jogadas salvam o Rei.

        :param casas_possiveis: Lista de casas possíveis de uma peça.
        :return: Lista de casas com potencial de salvar o Rei.
        """
        rei_da_vez: Rei = self.get_rei_da_vez()
        posicao_rei = rei_da_vez.posicao
        ameacantes: list[PecaBase] = rei_da_vez.ameacantes

        # Em casa_de_salvamento são incluídas todas as casas que estão entre o Rei ameaçado e o ameaçante desse Rei.
        casas_de_salvamento: list[Casa] = []

        # casas_de_defesa guarda todas as casas de salvamento que também estão em casas_possíveis.
        casas_de_defesa: list[Casa] = []

        for i in range(0, len(ameacantes)):
            posicao_ameacante = ameacantes[i].posicao
            casas_de_salvamento.append(self.vetor_de_Controle[posicao_ameacante[0]][posicao_ameacante[1]])

            # Verifica se estão na mesma linha
            if posicao_rei[0] == posicao_ameacante[0]:
                # verifica se o ameaçante está a direita ou a esquerda
                step = 1 if posicao_ameacante[1] > posicao_rei[1] else -1 
                # Varre as casas entre o rei e ameaçante e salva em casa_de_salvamento
                for coluna in range(posicao_rei[1] + step, posicao_ameacante[1]):
                    casas_de_salvamento.append(self.vetor_de_Controle[posicao_rei[0]][coluna])

            # Verifica se estão na mesma coluna
            elif posicao_rei[1] == posicao_ameacante[1]:
                # Verifica se o ameaçante está acima ou abaixo do rei
                step = 1 if posicao_ameacante[0] > posicao_rei[0] else -1
                # Varre as casas entre o rei e ameaçante e salva em casa_de_salvamento
                for linha in range(posicao_rei[0] + step, posicao_ameacante[0]):
                    casas_de_salvamento.append(self.vetor_de_Controle[linha][posicao_rei[1]])

            # Verifica se estão na mesma diagonal
            else:
                if type(ameacantes[i]) == Bispo or type(ameacantes[i]) == Rainha:
                    # Verifica em qual diagonal o ameaçante está
                    step_l = 1 if posicao_ameacante[0] > posicao_rei[0] else -1
                    step_c = 1 if posicao_ameacante[1] > posicao_rei[1] else -1
                    linha = posicao_rei[0] + step_l
                    coluna = posicao_rei[1] + step_c
                    # Varre as casas entre o rei e ameaçante e salva em casa_de_salvamento
                    while posicao_ameacante[0] != linha and posicao_ameacante[1] != coluna:
                        casas_de_salvamento.append(self.vetor_de_Controle[linha][coluna])
                        linha += step_l
                        coluna += step_c

        # Faz o cruzamento entre as casa possíveis e as casas de salvamento.
        # Caso uma casa esteja nos dois vetores ela é acrescentada no vetor casas_de_defesa.
        for i in range(0, len(casas_possiveis)):
            for j in range(0, len(casas_de_salvamento)):
                if casas_possiveis[i].posicao == casas_de_salvamento[j].posicao:
                    casas_de_defesa.append(casas_de_salvamento[j])

        return casas_de_defesa

    def tratar_xeque_em_potencial(self, peca_selecionada: PecaBase, casas_possiveis: list[Casa]):
        """
        Se a peça selecionada está entre o seu Rei e um possível ameaçante a lista de casas possíveis recebida
        é tratada e é retornada uma nova lista de casas possível na qual os movimentos não deixarão o seu Rei em perigo.
        Se a peça selecionada NÃO se encontra na condição relatada, é retornado o valor None.

        :param peca_selecionada: Peça que foi selecionada pelo jogador.
        :param casas_possiveis: Lista que será tratada.
        """
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
        """
        A partir da posição passada pega todas as casas acima até encontrar uma peça ou até terminar o tabuleiro.
        :param posicao_atual: Coordenada do tabuleiro que será usada como base.
        """
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
        """
        A partir da posição passada pega todas as casas abaixo até encontrar uma peça ou até terminar o tabuleiro.
        :param posicao_atual: Coordenada do tabuleiro que será usada como base.
        """
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
        """
        A partir da posição passada pega todas as casas a direita até encontrar uma peça ou até terminar o tabuleiro.
        :param posicao_atual: Coordenada do tabuleiro que será usada como base.
        """
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
        """
        A partir da posição passada pega todas as casas a esquerda até encontrar uma peça ou até terminar o tabuleiro.
        :param posicao_atual: Coordenada do tabuleiro que será usada como base.
        """
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
        """
        A partir da posição passada pega todas as casas na direção superior direita até encontrar uma peça
        ou até terminar o tabuleiro.
        :param posicao_atual: Coordenada do tabuleiro que será usada como base.
        """
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
        """
        A partir da posição passada pega todas as casas na direção inferior direita até encontrar uma peça
        ou até terminar o tabuleiro.
        :param posicao_atual: Coordenada do tabuleiro que será usada como base.
        """
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
        """
        A partir da posição passada pega todas as casas na direção inferior esquerda até encontrar uma peça
        ou até terminar o tabuleiro.
        :param posicao_atual: Coordenada do tabuleiro que será usada como base.
        """
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
        """
        A partir da posição passada pega todas as casas na direção superior esquerda até encontrar uma peça
        ou até terminar o tabuleiro.
        :param posicao_atual: Coordenada do tabuleiro que será usada como base.
        """
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

    def get_caminho_da_morte(self, posicao_peca: tuple[int, int]) -> list[Casa]:
        """
        Verifica se uma peça está entre seu Rei e um possível ameaçante.
        Se estiver, retorna a lista de casas entre o possível ameaçante e o Rei.

        :param posicao_peca: Posição da peça que será verificada
        :return:
        """
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
        """
        Verifica se houve xeque-mate.
        Se houve, mostra na tela a mensagem 'Xeque-Mate'.
        :return:
        """
        todas_casas_possiveis: list[Casa] = []

        for i in range(8):
            for j in range(8):
                if self.vetor_de_Controle[i][j].peca is not None:
                    peca = self.vetor_de_Controle[i][j].peca
                    if peca.tonalidade == self.vez:
                        casas_possiveis_peca = peca.get_casas_possiveis(self.vetor_de_Controle)
                        casas_possivel_cheque_tratadas = self.tratar_xeque_em_potencial(peca, todas_casas_possiveis)
                        if casas_possivel_cheque_tratadas is not None:
                            casas_possiveis_peca.clear()
                            casas_possiveis_peca.extend(casas_possivel_cheque_tratadas)
                        if self.rei_em_xeque() and type(self.vetor_de_Controle[i][j].peca) != Rei:
                            casas_tratadas = self.get_casas_que_salvam_o_rei(casas_possiveis_peca)
                            casas_possiveis_peca.clear()
                            casas_possiveis_peca.extend(casas_tratadas)
                        todas_casas_possiveis.extend(casas_possiveis_peca)

        if len(todas_casas_possiveis) == 0 and self.get_rei_da_vez().is_xeque():

            print("XEQUE-MATE!")
            return True
        return False

    def mostrar_msg_xeque_mate(self, jogador):
        """
        Quando chamado. Imprime na tela a mensagem 'Xeque-mate'
        :return:
        """
        txt = 'Vitória do jogador ' + jogador + '!!!'  ##### armazena o texto
        pygame.font.init()  ##### inicia font
        fonte = pygame.font.get_default_font()  ##### carrega com a fonte padrão
        fontesys = pygame.font.SysFont(fonte, 120)  ##### usa a fonte padrão
        txttela = fontesys.render(txt, 1,  (119, 221, 119))  ##### renderiza o texto na cor desejada
        self.display.blit(txttela, (150, 280))  ##### coloca na posição 50,900 (tela FHD)
        pygame.display.update()
        txt2 = 'XEQUE-MATE'  ##### armazena o texto
        pygame.font.init()  ##### inicia font
        fonte2 = pygame.font.get_default_font()  ##### carrega com a fonte padrão
        fontesys2 = pygame.font.SysFont(fonte2, 50)  ##### usa a fonte padrão
        txttela2 = fontesys2.render(txt2, 1, (255, 255, 255)) ##### renderiza o texto na cor desejada
        self.display.blit(txttela2, (470, 15))  ##### coloca na posição 50,900 (tela FHD)
        pygame.display.update()
        time.sleep(7)
        exit()
