from __future__ import annotations

import pygame
from appConstants import ImagesPath
from pecas_models.peao import Peao
from pecas_models.cavalo import Cavalo
from pecas_models.torre import Torre
from pecas_models.bispo import Bispo
from pecas_models.rainha import Rainha
from pecas_models.rei import Rei
from pecas_models.pecaBase import PecaBase


class Casa(pygame.sprite.Sprite):
    letrasColunas: list[str] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    numerosColunas: list[str] = ['8', '7', '6', '5', '4', '3', '2', '1']

    def __init__(
            self,
            *groups,
            display: pygame.Surface,
            posicao_na_matriz: (int, int)
    ):
        super().__init__(*groups)

        self._layer = 1

        self.selecionado: bool = False
        self.possivel: bool = False
        self.caminhoImagemFundo: str = ''
        self.posicao_na_matriz: tuple[int, int] = posicao_na_matriz
        self.peca: PecaBase = None
        self.is_roque: bool = False
        self.is_en_Passant: bool = False

        self.tamanho: int = int(display.get_height() / 10)
        x = (posicao_na_matriz[1] * self.tamanho) + ((display.get_width() - (self.tamanho * 8)) / 2)
        y = (posicao_na_matriz[0] * self.tamanho) + self.tamanho

        self.display = display
        self.posicao: str = Casa.letrasColunas[posicao_na_matriz[1]] + Casa.numerosColunas[posicao_na_matriz[0]]

        self.rect = pygame.Rect(x, y, self.tamanho, self.tamanho)

        primeiro_tom: str = 'claro' if (posicao_na_matriz[0] % 2 == 0) else 'escuro'
        segundo_tom: str = 'claro' if (primeiro_tom == 'escuro') else 'escuro'
        self.tonalidade: str = primeiro_tom if (posicao_na_matriz[1] % 2 == 0) else segundo_tom

        self.atualizar_imagem_de_fundo()

    def atualizar_imagem_de_fundo(self):
        if self.tonalidade == 'escuro':
            if self.possivel:
                self.caminhoImagemFundo = ImagesPath.QUADRADO_FULIGEM_POSSIVEL
            elif self.selecionado:
                self.caminhoImagemFundo = ImagesPath.QUADRADO_FULIGEM_SELECIONADO
            else:
                self.caminhoImagemFundo = ImagesPath.QUADRADO_FULIGEM
        elif self.tonalidade == 'claro':
            if self.possivel:
                self.caminhoImagemFundo = ImagesPath.QUADRADO_MADEIRA_POSSIVEL
            elif self.selecionado:
                self.caminhoImagemFundo = ImagesPath.QUADRADO_MADEIRA_SELECIONADO
            else:
                self.caminhoImagemFundo = ImagesPath.QUADRADO_MADEIRA

        self.image = pygame.image.load(self.caminhoImagemFundo)
        self.image = pygame.transform.scale(self.image, [self.tamanho, self.tamanho])

    def marcar_como_selecionado(self):
        self.selecionado = True
        self.atualizar_imagem_de_fundo()

    def desmarcar_como_selecionado(self):
        self.selecionado = False
        self.atualizar_imagem_de_fundo()

    def marcar_como_possivel(self):
        self.possivel = True
        self.atualizar_imagem_de_fundo()

    def desmarcar_como_possivel(self):
        self.possivel = False
        self.atualizar_imagem_de_fundo()

    def inserir_peca(self, peca: PecaBase):
        if self.peca is not None:
            self.peca.kill()

        self.peca = peca
        self.peca.rect.center = self.rect.copy().center
        self.peca.posicao[0] = self.posicao_na_matriz[0]
        self.peca.posicao[1] = self.posicao_na_matriz[1]

    def remover_peca(self):
        self.peca = None

    def carregar_peca(self):
        i: int = self.posicao_na_matriz[0]
        j: int = self.posicao_na_matriz[1]

        if 2 <= i <= 5:
            return
        
        # Peões pretos
        if i == 1:
            self.peca = Peao(self.groups(), rect_base=self.rect.copy(), tom='escuro', posicao=[i, j], casaOrigem=self.posicao)
            return
        # Peões brancos
        if i == 6:
            self.peca = Peao(self.groups(), rect_base=self.rect.copy(), tom='claro', posicao=[i, j], casaOrigem=self.posicao)
            return
        # Cavalo preto
        if (i == 0 and j == 1) or (i == 0 and j == 6):
            self.peca = Cavalo(self.groups(), rect_base=self.rect.copy(), tom='escuro', posicao=[i, j], casaOrigem=self.posicao)
            return
        # Cavalo claro
        if (i == 7 and j == 1) or (i == 7 and j == 6):
            self.peca = Cavalo(self.groups(), rect_base=self.rect.copy(), tom='claro', posicao=[i, j], casaOrigem=self.posicao)
            return
        
        # Torre preto
        if (i == 0 and j == 0) or (i == 0 and j == 7):
            self.peca = Torre(self.groups(), rect_base=self.rect.copy(), tom='escuro', posicao=[i, j], casaOrigem=self.posicao)
            return
        # Torre claro
        if (i == 7 and j == 0) or (i == 7 and j == 7):
            self.peca = Torre(self.groups(), rect_base=self.rect.copy(), tom='claro', posicao=[i, j], casaOrigem=self.posicao)
            return
        
        # Bispo preto
        if (i == 0 and j == 2) or (i == 0 and j == 5):
            self.peca = Bispo(self.groups(), rect_base=self.rect.copy(), tom='escuro', posicao=[i, j], casaOrigem=self.posicao)
            return
        # Bispo claro
        if (i == 7 and j == 2) or (i == 7 and j == 5):
            self.peca = Bispo(self.groups(), rect_base=self.rect.copy(), tom='claro', posicao=[i, j], casaOrigem=self.posicao)
            return
        # Rainha preto
        if (i == 0 and j == 3):
            self.peca = Rainha(self.groups(), rect_base=self.rect.copy(), tom='escuro', posicao=[i, j], casaOrigem=self.posicao)
            return
        # Rainha claro
        if (i == 7 and j == 3):
            self.peca = Rainha(self.groups(), rect_base=self.rect.copy(), tom='claro', posicao=[i, j], casaOrigem=self.posicao)
            return
        # Rei preto
        if (i == 0 and j == 4):
            self.peca = Rei(self.groups(), rect_base=self.rect.copy(), tom='escuro', posicao=[i, j], casaOrigem=self.posicao)
            return
        # Rei claro
        if (i == 7 and j == 4):
            self.peca = Rei(self.groups(), rect_base=self.rect.copy(), tom='claro', posicao=[i, j], casaOrigem=self.posicao)
            return
