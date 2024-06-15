import pygame
from settings import *
from board import Board


class Game:

    def __init__(self):
        self.board = Board()

    def show_board(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200) # light green square
                else:
                    color = (119, 154, 88) # dark green square
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

                pygame.draw.rect(surface, color, rect)
    
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # check if piece is on square
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    img = pygame.image.load(piece.image_url) # Render image
                    img_center = col*SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2 # Center image
                    piece.texture_rect = img.get_rect(center=img_center)
                    surface.blit(img, piece.texture_rect) # Blit image into square

            

