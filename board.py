from settings import *
from square import Square
from piece import *
from move import Move
import copy
from sound import Sound
import os

class Board:

    # Initialization of the board and the pieces
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for _ in range(COLS)]
        self.last_move = None
        self.create() # Creates the board
        self.add_pieces("white")
        self.add_pieces("black")
    
    # Creates the squares which makes up the board
    def create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    # Adds the pieces to their starting positions
    def add_pieces(self, color):

        if color == "white":
            row_pawn, row_other = (6, 7) # white pawns on row 6, other pieces on row 7
        else:
            row_pawn, row_other = (1, 0) # black pawns on row 1, others on row 0
        
        # Pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))


        # Knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        # Rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        # Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        # King
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    def castling(self, initial, final): 
        # If king moves by more than 2 squares = castling
        return abs(initial.col - final.col) == 2
    
    def set_true_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return
        
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        piece.en_passant = True

    # move piece
    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.col].isfree()

        #Update the board after move
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece


        if isinstance(piece, Pawn):
            # En passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(os.path.join(
                        'assets/sounds/capture.wav'
                    ))
                    sound.play()
            else:
            # pawn promotion
                self.check_promotion(piece, final)
        
        # Castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.valid_moves[-1])
                # play sound
                sound = Sound(os.path.join(
                    'assets/sounds/castling.wav'
                ))
                sound.play()
        
        # move
        piece.moved = True
        
        # clear valid moves
        piece.clear_moves()
        self.last_move = move

    # Check if move is valid
    def valid_move(self, piece, move) -> bool:
        return move in piece.valid_moves


    # Promotes pawn to queen if pawn reaches final row
    def check_promotion(self, piece, final) -> None:
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    # Method for checking checks
    def is_in_check(self, color, move=None, piece=None) -> bool:
        board = self

        if move is not None and piece is not None:
            temp_piece = copy.deepcopy(piece)
            temp_board = copy.deepcopy(self)
            temp_board.move(temp_piece, move, testing=True)
            board = temp_board

        # Find position of the king for the given color
        king_pos = None
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    board_piece = board.squares[row][col].piece
                    if isinstance(board_piece, King) and board_piece.color == color:
                        king_pos = (row, col)
                        break
            if king_pos:
                break

        if not king_pos:
            return False

        king_row, king_col = king_pos
        # Scan all enemy pieces
        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_enemy_piece(color):
                    enemy = board.squares[row][col].piece
                    # Just to be safe
                    enemy.clear_moves()
                    # valid moves for the enemy piece
                    board.calc_moves(enemy, row, col, bool=False)
                    for enemy_move in enemy.valid_moves:
                        # Check
                        if enemy_move.final.row == king_row and enemy_move.final.col == king_col:
                            enemy.clear_moves()
                            print(f"{color} King is checked at {Square.get_alphacol(king_col)}{king_row} by {enemy}")
                            return True
                    enemy.clear_moves()

        return False

    def game_over(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    if self.squares[row][col].piece.valid_moves == []:
                        return True
        return False


    # Calculate possible valid moves
    def calc_moves(self, piece, row, col, bool=True):
        '''
        Calculate all possible valid moves for a 
        specific piece on a specific position
        '''

        # Clear previous moves to remove stale moves from previous states
        piece.clear_moves()

        def king_moves():
            adjacent = [
                (row-1, col+0), # up
                (row-1, col+1), #up-right
                (row+0, col+1), #right
                (row+1, col+1), #down-right
                (row+1, col+0), #down
                (row+1, col-1), #down-left
                (row+0, col-1), #left
                (row-1, col-1) #up-left
            ]
            # Normal moves
            for possible_move in adjacent:
                move_row, move_col = possible_move
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isfree_or_enemy(piece.color):
                        # create new move
                        initial = Square(row, col)
                        final_piece = self.squares[move_row][move_col].piece
                        final = Square(move_row, move_col, final_piece)
                        move = Move(initial, final)
                        # Check for potential checks (pins and forks)
                        if bool:
                            if not self.is_in_check(piece.color, move, piece):
                                # append new valid move
                                piece.add_moves(move)
                            else:
                                break
                        else:
                            piece.add_moves(move)
                        
            
            # Castling
            if not piece.moved:
                # Queen-side
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece(): # Castling not possible if pieces are in the way
                                break
                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                move_rook = Move(initial, final)
                                left_rook.add_moves(move_rook)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                move_king = Move(initial, final)
                                # Check for potential checks (pins and forks)
                                if bool:
                                    if not self.is_in_check(piece.color, move_king, piece) and not self.is_in_check(left_rook.color, move_rook, left_rook):
                                        left_rook.add_moves(move_rook)
                                        # append new valid move
                                        piece.add_moves(move_king)
                                else:
                                    left_rook.add_moves(move_rook)
                                    piece.add_moves(move_king)
                # King-side
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece(): # Castling not possible if pieces are in the way
                                break
                            if c == 6:
                                # adds right rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                move_rook = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                move_king = Move(initial, final)
                                # Check for potential checks (pins and forks)
                                if bool:
                                    if not self.is_in_check(piece.color, move_king, piece) and not self.is_in_check(right_rook.color, move_rook, right_rook):
                                        # append new valid move
                                        right_rook.add_moves(move_rook)
                                        piece.add_moves(move_king)
                                else:
                                    right_rook.add_moves(move_rook)
                                    piece.add_moves(move_king)
            moves = [[f"{Square.get_alphacol(move.initial.col)} {move.initial.row}", 
                      f"{Square.get_alphacol(move.final.col)} {move.final.row}"] for move in piece.valid_moves]
            print(f"Moves for {str(piece)}: {moves}")


        def knight_moves():
            possible_moves = [
                (row-2, col+1),
                (row-2, col-1),
                (row-1, col-2),
                (row-1, col+2),
                (row+1, col-2),
                (row+1, col+2),
                (row+2, col-1),
                (row+2, col+1)
            ]
            for possible_move in possible_moves:
                move_row, move_col = possible_move
                # if move is not outside of the board
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isfree_or_enemy(piece.color):
                        # create new move
                        final_piece = self.squares[move_row][move_col].piece
                        initial = Square(row, col)
                        final = Square(move_row, move_col, final_piece)
                        move = Move(initial, final)
                        # Check for potential checks (pins and forks)
                        if bool:
                            if not self.is_in_check(piece.color, move, piece):
                                # append new valid move
                                piece.add_moves(move)
                        else:
                            piece.add_moves(move)

        def straightline_moves(increments):
            for incr in increments:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # Create new possible move
                        move = Move(initial, final)
                        # if square is free
                        if self.squares[possible_move_row][possible_move_col].isfree():
                            # Check for potential checks (pins and forks)
                            if bool:
                                if not self.is_in_check(piece.color, move, piece):
                                    # append new valid move
                                    piece.add_moves(move)
                            else:
                                piece.add_moves(move)

                        # has enemy piece = add move and break
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # Check for potential checks (pins and forks)
                            if bool:
                                if not self.is_in_check(piece.color, move, piece):
                                    # append new valid move
                                    piece.add_moves(move)
                            else:
                                piece.add_moves(move)
                            break
                        # has friendly piece
                        elif self.squares[possible_move_row][possible_move_col].has_friendly_piece(piece.color):
                            break
                    # out of bounds
                    else:
                        break
                    # incrementing
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr
        def bishop_moves():
            straightline_moves([
                (-1, 1), #up-right
                (-1, -1), #up-left
                (1, 1), #down-right
                (1, -1) #down-left
            ])
        def pawn_moves():
            piece = self.squares[row][col].piece
            if piece.color == 'black':
                if row != 1: piece.moved = True
            if piece.color == 'white':
                if row != 6: piece.moved = True
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1+steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isfree():
                        # create move
                        initial = Square(row, col)
                        final_piece = self.squares[move_row][col].piece
                        final = Square(move_row, col, final_piece)
                        move = Move(initial, final)
                        #piece.add_moves(move)

                        # Check for potential checks (pins and forks)
                        if bool:
                            if not self.is_in_check(piece.color, move, piece):
                                # append new valid move
                                piece.add_moves(move)
                        else:
                            piece.add_moves(move)
                    # pawn is blocked
                    else:
                        break
                # out of bounds
                else:
                    break
            
            # Diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        move = Move(initial, final)
                        # Check for potential checks (pins and forks)
                        if bool:
                            if not self.is_in_check(piece.color, move, piece):
                                # append new valid move
                                piece.add_moves(move)
                        else:
                            piece.add_moves(move)

            # En passant moves
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            # left en passant
            if Square.in_range(col-1) and row == r:
                if self.squares[row][col-1].has_enemy_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final = Square(fr, col-1, p)
                            move = Move(initial, final)

                            if bool:
                                if not self.is_in_check(p.color, move, p):
                                    piece.add_moves(move)
                            else:
                                piece.add_moves(move)
            
            # right en passant
            if Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_enemy_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final = Square(fr, col+1, p)
                            move = Move(initial, final)

                            if bool:
                                if not self.is_in_check(p.color, move, p):
                                    piece.add_moves(move)
                            else:
                                piece.add_moves(move)
            
        def rook_moves():
            straightline_moves([
                (-1, 0), #up
                (0, 1), #left
                (1, 0), #down
                (0, -1) #right
            ])
        def queen_moves():
            straightline_moves([
                (-1, 1), #up-right
                (-1, -1), #up-left
                (1, 1), #down-right
                (1, -1), #down-left
                (-1, 0), #up
                (0, 1), #left
                (1, 0), #down
                (0, -1) #right
            ])


        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            bishop_moves()
        elif isinstance(piece, Rook):
            rook_moves()
        elif isinstance(piece, Queen):
            queen_moves()
        elif isinstance(piece, King):
            king_moves()
