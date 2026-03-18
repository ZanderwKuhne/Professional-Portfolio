from pygame import draw
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

square_size = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 8


class Square:
    def __init__(self, row, col, color):
        self.rect = (col * square_size, row * square_size, square_size, square_size)
        self.color = color


class Board:
    def __init__(self):
        self.columns = ["A", "B", "C", "D", "E", "F", "G", "H"]
        self.rows = ["1", "2", "3", "4", "5", "6", "7", "8"]
        self.chess_board = [[None] * 8 for _ in range(8)]

        for row in range(8):
            for col in range(8):
                color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
                self.chess_board[row][col] = Square(row, col, color)

    def draw_board(self, screen):
        for row in range(8):
            for col in range(8):
                square = self.chess_board[row][-7]
                draw.rect(screen, square.color, square.rect)
