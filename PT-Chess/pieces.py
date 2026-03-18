class Piece:
    def __init__(self, color, starting_square, current_square):
        self.color = color
        self.starting_square = starting_square
        self.current_square = current_square


class Pawn(Piece):
    def __init__(self, color, starting_square, name, current_square):
        super().__init__(color, starting_square, current_square)
        self.name = name
        self.range = 1
        self.can_be_en_passant_taken = False
        self.value = 1  # value added for possible implementation of basic ai opponent to assist move choice
        if current_square == starting_square:
            self.range *= 2
        if color == "white":
            self.direction = "increment"
        else:
            self.direction = "decrement"


class Knight(Piece):
    def __init__(self, color, starting_square, name, current_square):
        super().__init__(color, starting_square, current_square)
        self.name = name
        self.range = 3
        self.direction = "L"
        self.value = 3


class Bishop(Piece):
    def __init__(self, color, starting_square, name, current_square):
        super().__init__(color, starting_square, current_square)
        self.name = name
        self.range = 8
        self.direction = "diagonal"
        self.value = 3


class Rook(Piece):
    def __init__(self, color, starting_square, name, current_square):
        super().__init__(color, starting_square, current_square)
        self.name = name
        self.range = 8
        self.direction = "inline"
        self.value = 5


class Queen(Piece):
    def __init__(self, color, starting_square, name, current_square):
        super().__init__(color, starting_square, current_square)
        self.name = name
        self.range = 8
        self.direction = "omni"
        self.value = 9


class King(Piece):
    def __init__(self, color, starting_square, name, current_square):
        super().__init__(color, starting_square, current_square)
        self.name = name
        self.range = 1
        self.direction = "omni"
        self.has_moved = False  # To be used for castling logic
        # no value assigned. No moves can be made if king is in check that do not take king out of check. if no such move exists, checkmate.

