import pygame

from appConstants import ImagesPath

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

        self.selecionado: bool = False
        self.possivel: bool = False
        self.caminhoImagemFundo: str = ''
        self.posicao_na_matriz: tuple(int, int) = posicao_na_matriz

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
