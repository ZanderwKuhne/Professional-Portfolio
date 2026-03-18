import board
import pygame
from constants import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    gamefont = pygame.font.SysFont(None, 30)
    chess_board = board.Board()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        chess_board.draw_board(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


main()
