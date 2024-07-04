import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
class Piece:
    
    def __init__(self, name, color, value, image_url=None, texture_rect=None):
        self.name = name
        self.color = color
        if color == "white":
            value_sign = 1
        else:
            value_sign = -1
        self.value =  value * value_sign
        self.valid_moves = []
        self.moved = False
        self.image_url = image_url
        self.set_texture()
        self.texture_rect = texture_rect

    # Sets the different images of the pieces
    def set_texture(self, size=80):
        self.image_url = os.path.join(
            f"assets/images/imgs-{size}px/{self.color}_{self.name}.png"
        )
    
    def add_moves(self, move):
        self.valid_moves.append(move)
    
    def clear_moves(self):
        self.valid_moves = []

# The different pieces inherits the Piece class
class Pawn(Piece):
    def __init__(self, color):
        if color == "white":
            self.dir = -1
        else:
            self.dir = 1
        super().__init__("pawn", color, 1.0)

class Knight(Piece):
    def __init__(self, color):
        super().__init__("knight", color, 3.0)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__("bishop", color, 3.001)

class Rook(Piece):
    def __init__(self, color):
        super().__init__("rook", color, 5.0)
    
class Queen(Piece):
    def __init__(self, color):
        super().__init__("queen", color, 9.0)

class King(Piece):
    def __init__(self, color):
        super().__init__("king", color, 10000)

