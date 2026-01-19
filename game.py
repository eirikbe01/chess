import pygame
from settings import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square
from sound import Sound

class Game:

    def __init__(self):
        self.next_player = 'white'
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    def show_board(self, surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = theme.bg.light
                else:
                    color = theme.bg.dark
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

                pygame.draw.rect(surface, color, rect)
                # Row coordinates
                if col == 0:
                    # Color
                    if row % 2 == 0:
                        color = theme.bg.dark
                    else:
                        color = theme.bg.light
                    # Label 
                    label = self.config.font.render(str(ROWS-row), 1, color)
                    label_pos = (5, 5 + row*SQUARE_SIZE)
                    # blit
                    surface.blit(label, label_pos)
                # Column coordinates
                if row == 7:
                    # Color
                    if (row + col) % 2 == 0:
                        color = theme.bg.dark
                    else:
                        color = theme.bg.light
                    # Label 
                    label = self.config.font.render(Square.get_alphacol(col), 1, color)
                    label_pos = (col * SQUARE_SIZE + SQUARE_SIZE - 20, HEIGHT-20)
                    # blit
                    surface.blit(label, label_pos)

    
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
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # Loop through all valid moves for the piece
            for move in piece.valid_moves:
                # color
                if (move.final.row + move.final.col) % 2 == 0:
                    color = theme.moves.light
                else:
                    color = theme.moves.dark
                # rect
                rect = (move.final.col * SQUARE_SIZE, move.final.row * SQUARE_SIZE,
                        SQUARE_SIZE, SQUARE_SIZE)
                # blit
                pygame.draw.rect(surface, color, rect)
    
    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for pos in [initial, final]:
                # color
                if (pos.row + pos.col) % 2 == 0:
                    color = theme.trace.light
                else: 
                    color = theme.trace.dark
                # rect
                rect = (pos.col * SQUARE_SIZE, pos.row * SQUARE_SIZE, 
                        SQUARE_SIZE, SQUARE_SIZE)
                #blit
                pygame.draw.rect(surface, color, rect)
    
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
    
    def change_theme(self):
        self.config.change_theme()
    
    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def play_check(self):
        self.config.check_sound.play()

    def restart(self):
        self.__init__()
        self.config.start_sound.play()


                

