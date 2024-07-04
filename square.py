
class Square:

    ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = self.ALPHACOLS[col]
    
    # Equals method for comparing rows and cols
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    # Checks if piece is on a square
    def has_piece(self):
        return self.piece != None
    
    # Check if square is free
    def isfree(self):
        return not self.has_piece()
    
    # Check if square has friendly piece
    def has_friendly_piece(self, color):
        return self.has_piece() and self.piece.color == color
    
    # Check if square has enemy piece
    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color
    
    # Check if square is free or has enemy piece
    def isfree_or_enemy(self, color):
        return self.isfree() or self.has_enemy_piece(color)
    
    # Static method which checks that moves does not go out of bounds of the board
    @staticmethod
    def in_range(*args):
        for arg in args:
            # if row or column is outside of the board
            if arg < 0 or arg > 7:
                return False
        return True
    
    @staticmethod
    def get_alphacol(col):
        ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return ALPHACOLS[col]
    
