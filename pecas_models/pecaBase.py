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

    @abc.abstractmethod
    def get_casas_possiveis(self, tabuleiro: list[list[Casa]], incluir_casas_ameacadas: bool = False) -> list[Casa]:
        pass

    @abc.abstractmethod
    def carregar_imagem(self, rect_base: pygame.Rect) -> None:
        pass
