from settings import *
from square import Square
from piece import *
from move import Move
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

    # move piece
    def move(self, piece, move):
        initial = move.initial
        final = move.final

        #Update the board after move
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # pawn promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)
        
        # Castling
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.valid_moves[-1])


        # move
        piece.moved = True
        
        # clear valid moves
        piece.clear_moves()
        self.last_move = move

    # Check if move is valid
    def valid_move(self, piece, move):
        return move in piece.valid_moves

    # Promotes pawn to queen if pawn reaches final row
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
    
    # Moves    
    def knight_moves(self, piece, row, col):
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
                    initial = Square(row, col)
                    final = Square(move_row, move_col)
                    move = Move(initial, final)
                    # Append the valid move
                    piece.add_moves(move)
    def straightline_moves(self, increments, piece, row, col):
        for incr in increments:
            row_incr, col_incr = incr
            possible_move_row = row + row_incr
            possible_move_col = col + col_incr

            while True:
                if Square.in_range(possible_move_row, possible_move_col):
                    initial = Square(row, col)
                    final = Square(possible_move_row, possible_move_col)
                    # Create new possible move
                    move = Move(initial, final)
                    # if square is free
                    if self.squares[possible_move_row][possible_move_col].isfree():
                        piece.add_moves(move)

                    # has enemy piece = add move and break
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # append new possible move
                        piece.add_moves(move)
                        break
                    # has friendly piece
                    if self.squares[possible_move_row][possible_move_col].has_friendly_piece(piece.color):
                        break
                # out of bounds
                else:
                    break
                # incrementing
                possible_move_row = possible_move_row + row_incr
                possible_move_col = possible_move_col + col_incr
    def bishop_moves(self, piece, row, col):
        self.straightline_moves([
            (-1, 1), #up-right
            (-1, -1), #up-left
            (1, 1), #down-right
            (1, -1) #down-left
        ], piece, row, col)
    def pawn_moves(self, piece, row, col):
        steps = 1 if piece.moved else 2

        # vertical moves
        start = row + piece.dir
        end = row + (piece.dir * (1+steps))

        for move_row in range(start, end, piece.dir):
            if Square.in_range(move_row):
                if self.squares[move_row][col].isfree():
                    # create move
                    initial = Square(row, col)
                    final = Square(move_row, col)
                    move = Move(initial, final)
                    # Append valid move 
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
                    final = Square(possible_move_row, possible_move_col)
                    move = Move(initial, final)
                    # append new move
                    piece.add_moves(move)
    def rook_moves(self, piece, row, col):
        self.straightline_moves([
            (-1, 0), #up
            (0, 1), #left
            (1, 0), #down
            (0, -1) #right
        ], piece, row, col)
    def queen_moves(self, piece, row, col):
        self.straightline_moves([
            (-1, 1), #up-right
            (-1, -1), #up-left
            (1, 1), #down-right
            (1, -1), #down-left
            (-1, 0), #up
            (0, 1), #left
            (1, 0), #down
            (0, -1) #right
        ], piece, row, col)
    def king_moves(self, piece, row, col):
        adjacent = [
            (row-1, col), # up
            (row-1, col+1), #up-right
            (row-1, col-1), #up-left
            (row+1, col), #down
            (row+1, col+1), #down-right
            (row+1, col-1), #down-left
            (row, col-1), #left
            (row, col+1), #right
        ]
        # Normal moves
        for possible_move in adjacent:
            move_row, move_col = possible_move
            # If the square is in range...
            if Square.in_range(move_row, move_col):
                # ..and if square is free or has an enemy, create valid move
                if self.squares[move_row][move_col].isfree_or_enemy(piece.color):
                    # create new move
                    initial = Square(row, col)
                    final = Square(move_row, move_col)
                    move = Move(initial, final)
                    # append to possible valid moves
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
                            move = Move(initial, final)
                            left_rook.add_moves(move)


                            # king move
                            initial = Square(row, col)
                            final = Square(row, 2)
                            move = Move(initial, final)
                            piece.add_moves(move)
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
                            move = Move(initial, final)
                            right_rook.add_moves(move)


                            # king move
                            initial = Square(row, col)
                            final = Square(row, 6)
                            move = Move(initial, final)
                            piece.add_moves(move)

    def castling(self, initial, final):
        # If king moves by more than 2 squares = castling
        return abs(initial.col - final.col) == 2
    
    # Calculate possible valid moves
    def calc_moves(self, piece, row, col):
        '''
        Calculate all possible valid moves for a 
        specific piece on a specific position
        '''
        if isinstance(piece, Pawn):
            self.pawn_moves(piece, row, col)
        elif isinstance(piece, Knight):
            self.knight_moves(piece, row, col)
        elif isinstance(piece, Bishop):
            self.bishop_moves(piece, row, col)
        elif isinstance(piece, Rook):
            self.rook_moves(piece, row, col)
        elif isinstance(piece, Queen):
            self.queen_moves(piece, row, col)
        elif isinstance(piece, King):
            self.king_moves(piece, row, col)
