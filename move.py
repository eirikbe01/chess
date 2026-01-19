class Move:
    
    def __init__(self, initial, final):
        # Initial square and final square
        self.initial = initial
        self.final = final

    # Equals method for comparing moves
    def __eq__(self, other):
        return (self.initial == other.initial) and (self.final == other.final)
    
    def __str__(self):
        return f"{self.initial}, {self.final}"

