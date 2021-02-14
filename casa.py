import pygame


class Casa(pygame.sprite.Sprite):

    def __init__(
            self,
            *groups,
            display: pygame.Surface,
            posicao_na_matriz: (int, int)
    ):
        super().__init__(*groups)

        primeiro_tom: str = 'claro' if (posicao_na_matriz[0] % 2 == 0) else 'escuro'
        segundo_tom: str = 'claro' if (primeiro_tom == 'escuro') else 'escuro'
        tonalidade: str = primeiro_tom if (posicao_na_matriz[1] % 2 == 0) else segundo_tom

        if tonalidade == 'escuro':
            self.caminhoImagemFundo = 'data/images/square-fuligem.png'
        elif tonalidade == 'claro':
            self.caminhoImagemFundo = 'data/images/square-madeira.png'

        tamanho: int = int(display.get_height() / 10)
        x = (posicao_na_matriz[0] * tamanho) + ((display.get_width() - (tamanho * 8)) / 2)
        y = (posicao_na_matriz[1] * tamanho) + tamanho

        self.image = pygame.image.load(self.caminhoImagemFundo)
        self.image = pygame.transform.scale(self.image, [tamanho, tamanho])
        self.rect = pygame.Rect(x, y, tamanho, tamanho)
