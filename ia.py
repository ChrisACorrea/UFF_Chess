from __future__ import annotations

import pygame
import random

class IA(pygame.sprite.Sprite):
    def __init__(
            self,
            tabuleiro
    ):
        self.jogador_vs_ia(tabuleiro)

    def jogador_vs_ia(self, tabuleiro):
        if tabuleiro.vez == "claro":
            return
        maior = 0
        casa_destino = None
        casa_origem = None
        jogadas_aleatorias_possiveis = []

        # selecionar jogada que captura a melhor peça, se houver, ou adicionar as jogadas possíveis a um vetor
        for i in range(8):
            for j in range(8):
                if tabuleiro.vetor_de_Controle[i][j].peca is not None:
                    peca = tabuleiro.vetor_de_Controle[i][j].peca
                    if peca.tonalidade == tabuleiro.vez:
                        for casa in peca.get_casas_possiveis(tabuleiro.vetor_de_Controle):
                            # tentando selecionar jogada que captura a melhor peça, se houver
                            if casa.peca is not None and casa.peca.tonalidade == "claro":
                                if (casa.peca.valor >= maior):
                                    maior = casa.peca.valor
                                    casa_destino = casa
                                    casa_origem = tabuleiro.vetor_de_Controle[i][j]
                        if peca is not None and len(peca.get_casas_possiveis(tabuleiro.vetor_de_Controle)) > 0:
                            jogadas_aleatorias_possiveis.append(tabuleiro.vetor_de_Controle[i][j])


        if casa_destino is None and casa_origem is None:
            tam_origem = len(jogadas_aleatorias_possiveis)
            index = random.randrange(0, tam_origem, 1)
            casa_origem = jogadas_aleatorias_possiveis[index]
            casa_origem.marcar_como_selecionado()

            tam_destino = len(casa_origem.peca.get_casas_possiveis(tabuleiro.vetor_de_Controle))
            index_destino = random.randrange(0, tam_destino, 1)
            casa_destino = casa_origem.peca.get_casas_possiveis(tabuleiro.vetor_de_Controle)[index_destino]
            
        casa_destino.marcar_como_possivel()    
        tabuleiro.casa_selecionada = casa_origem    
        tabuleiro.casas_possiveis = tabuleiro.casa_selecionada.peca.get_casas_possiveis(tabuleiro.vetor_de_Controle)
        tabuleiro.selecionar_casa(casa_destino, casa_destino.posicao_na_matriz)
        tabuleiro.limpar_selecoes()