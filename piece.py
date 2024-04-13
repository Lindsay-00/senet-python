from constants import BOARD_ORIGIN_X, BOARD_ORIGIN_Y, SQUARE_SIZE, PADDING, BLACK, TILE_MARGIN
import pygame


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.finished = False
        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        self.x = BOARD_ORIGIN_X + SQUARE_SIZE * self.col + SQUARE_SIZE // 2 + self.col * TILE_MARGIN
        self.y = BOARD_ORIGIN_Y + SQUARE_SIZE * self.row + SQUARE_SIZE // 2 + self.row * TILE_MARGIN

    def draw(self, window):
        radius = SQUARE_SIZE // 2 - PADDING * 2
        pygame.draw.circle(window, BLACK, (self.x, self.y), radius + 2)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calculate_position()
        
    def __repr__(self):
        return f"Piece({self.row}, {self.col}, {self.color})"
