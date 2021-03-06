from __future__ import annotations

import abc  # Abstract Base Classes
import pygame
from pygame.sprite import AbstractGroup


class PecaBase(pygame.sprite.Sprite, metaclass=abc.ABCMeta):

    def __init__(self, *groups: AbstractGroup, rect_base: pygame.Rect, tom: str, posicao: tuple[int, int], casaOrigem: str):
        super().__init__(*groups)

        self._layer = 2

        self.__id: str = self.__class__.__name__ + ' ' + tom + ' ' + casaOrigem
        self.__caminho_imagem: str = ''
        self.__tonalidade: str = tom
        self.__posicao: tuple[int, int] = posicao
        self.__movimentos: int = 0
        self.__valor: int = 0

        self.rect = pygame.rect.Rect(rect_base.x, rect_base.y, rect_base.width / 1.6, rect_base.height / 1.3)
        self.rect.center = rect_base.center

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def tonalidade(self):
        return self.__tonalidade

    @tonalidade.setter
    def tonalidade(self, tom):
        self.__tonalidade = tom

    @property
    def caminho_imagem(self):
        return self.__caminho_imagem

    @caminho_imagem.setter
    def caminho_imagem(self, caminho):
        self.__caminho_imagem = caminho

    @property
    def posicao(self):
        return self.__posicao

    @posicao.setter
    def posicao(self, posicao):
        self.__posicao = posicao

    @property
    def movimentos(self):
        return self.__movimentos

    @movimentos.setter
    def movimentos(self, movimentos):
        self.__movimentos = movimentos

    @property
    def valor (self):
        return self.__valor

    @valor.setter
    def valor (self, valor):
        self.__valor = valor

    @abc.abstractmethod
    def get_casas_possiveis(self, tabuleiro: list[list[Casa]], incluir_casas_ameacadas: bool = False) -> list[Casa]:
        """
        Pega todas as casas nas quais a peça pode ser jogada.

        :param tabuleiro: Matriz de controle que contém o estado do jogo.

        :param incluir_casas_ameacadas: Padrão: False. Se True for passado, será incluso na lista de casas possíveis
            as casas com potencial de serem possíveis, ou seja, na prática são casas que a peça atual não poderia ir,
            pois existe uma peça do mesmo time nela, mas que seria possível se nessa casa estivesse uma peça do time
            adversário.

        :return: Lista de casas em que a peça pode ser jogada.
        """
        pass

    @abc.abstractmethod
    def carregar_imagem(self, rect_base: pygame.Rect) -> None:
        pass
