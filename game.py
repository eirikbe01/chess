import pygame
from settings import *
from board import Board
from dragger import Dragger

class Game:

    def __init__(self):
        self.next_player = 'white'
        self.board = Board()
        self.dragger = Dragger()

    def show_board(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200) # white square
                else:
                    color = (119, 154, 88) # green square
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

                pygame.draw.rect(surface, color, rect)
    
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # check if piece is on square
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # all pieces except dragged piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.image_url) # Render image
                        img_center = col*SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2 # Center image
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect) # Blit image into square

    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            # Loop through all valid moves for the piece
            for move in piece.valid_moves:
                # color
                if (move.final.row + move.final.col) % 2 == 0:
                    color = '#C86464'
                else:
                    color = '#C84646'
                # rect
                rect = (move.final.col * SQUARE_SIZE, move.final.row * SQUARE_SIZE,
                        SQUARE_SIZE, SQUARE_SIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

                


