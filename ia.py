from __future__ import annotations

import pygame
import random

from casa import Casa


class IA(pygame.sprite.Sprite):
    def __init__(
            self,
            tabuleiro,
            modo_de_jogo
    ):
        self.iniciar_ia(tabuleiro, modo_de_jogo)

    def movimento_peca(self, tabuleiro, cor):
        if tabuleiro.vez != cor:
            return
        maior = 0
        casa_destino: Casa = None
        casa_origem: Casa = None
        jogadas_aleatorias_possiveis = []

        # selecionar jogada que captura a melhor peça, se houver, ou adicionar as jogadas possíveis a um vetor
        for i in range(8):
            for j in range(8):
                if tabuleiro.vetor_de_Controle[i][j].peca is not None:
                    peca = tabuleiro.vetor_de_Controle[i][j].peca
                    casa_selecionada: Casa = tabuleiro.vetor_de_Controle[i][j]
                    if peca.tonalidade == tabuleiro.vez:
                        tabuleiro.selecionar_casa(None, casa_selecionada.posicao_na_matriz)
                        for casa in tabuleiro.casas_possiveis:
                            # tentando selecionar jogada que captura a melhor peça, se houver
                            if casa.peca is not None and casa.peca.tonalidade != cor:
                                if (casa.peca.valor >= maior):
                                    maior = casa.peca.valor
                                    casa_destino = casa
                                    casa_origem = tabuleiro.vetor_de_Controle[i][j]
                        if peca is not None and len(tabuleiro.casas_possiveis) > 0:
                            jogadas_aleatorias_possiveis.append(tabuleiro.vetor_de_Controle[i][j])
                        tabuleiro.limpar_selecoes()


        if casa_destino is None and casa_origem is None:
            tam_origem = len(jogadas_aleatorias_possiveis)
            if(tam_origem > 0):
                index = random.randrange(0, tam_origem, 1)
            else:
                tabuleiro.fim_jogo()
            casa_origem = jogadas_aleatorias_possiveis[index]
            # casa_origem.marcar_como_selecionado()
            tabuleiro.selecionar_casa(None, casa_origem.posicao_na_matriz)

            tam_destino = len(tabuleiro.casas_possiveis)
            index_destino = random.randrange(0, tam_destino, 1)
            casa_destino = tabuleiro.casas_possiveis[index_destino]
            tabuleiro.limpar_selecoes()

        # casa_destino.marcar_como_possivel()
        tabuleiro.selecionar_casa(None, casa_origem.posicao_na_matriz)
        #tabuleiro.casa_selecionada = casa_origem
        #tabuleiro.casas_possiveis = tabuleiro.casa_selecionada.peca.get_casas_possiveis(tabuleiro.vetor_de_Controle)
        # tabuleiro.selecionar_casa(casa_origem, casa_destino.posicao_na_matriz)
        # tabuleiro.casas_possiveis = tabuleiro.casa_selecionada.peca.get_casas_possiveis(tabuleiro.vetor_de_Controle)
        tabuleiro.selecionar_casa(None, casa_destino.posicao_na_matriz)
        #tabuleiro.limpar_selecoes()

    def jogador_vs_ia(self, tabuleiro):
        self.movimento_peca(tabuleiro, "escuro")

    def ia_vs_ia(self, tabuleiro):
        self.movimento_peca(tabuleiro, "claro")
        self.movimento_peca(tabuleiro, "escuro")

    def iniciar_ia(self, tabuleiro, modo_de_jogo):
        if modo_de_jogo == 2:
            self.jogador_vs_ia(tabuleiro)
        elif modo_de_jogo == 3:
            self.ia_vs_ia(tabuleiro)

    def total_de_movimentos(self, tabuleiro):
        movimentos = 0
        for i in range(8):
            for j in range(8):
                if tabuleiro.vetor_de_Controle[i][j].peca is not None:
                    peca = tabuleiro.vetor_de_Controle[i][j].peca
                    movimentos += peca.movimentos

        print("TOTAL DE MOVIMENTOS:", movimentos)