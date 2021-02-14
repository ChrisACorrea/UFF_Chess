import pygame

from casa import Casa
from tabuleiro import Tabuleiro

# Inicializando Pygame
pygame.init()
# Criando a janela
display = pygame.display.set_mode([800, 600])
# Trocando o título
windowIcon = pygame.image.load('data/images/chess-solid-black.png')
pygame.display.set_caption("UFF Chess", 'data/images/chess-solid-black.png')
pygame.display.set_icon(windowIcon)

gameLoop: bool = True
clock = pygame.time.Clock()

tabuleiro = Tabuleiro(display=display)

def draw():
    display.fill([46, 46, 46])

    Tabuleiro.desenharTabuleiro()

    pygame.display.update()


if __name__ == '__main__':
    while gameLoop:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = False

        draw()
        pygame.display.update()
