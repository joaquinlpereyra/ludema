class _GameError(Exception):
    def __init__(self):
        pass

class PieceDoesNotHaveItemError(_GameError):
    def __init__(self, piece, item):
        _GameError.__init__(self)
        self.piece = piece
        self.item = item

    def __str__(self):
        error_string = ("The Piece {0} doesn't have item {1}"
                        .format(self.piece.name, self.item.name))
        return error_string

class PieceIsNotOnATileError(_GameError):
    def __init__(self, piece):
        _GameError.__init__(self)
        self.piece = piece

    def __str__(self):
        error_string = ("The Piece {0} isn't on a tile. Pieces must be "
                        "put on a tile the Board.put_piece method "
                        "before they can move.".format(self.piece.name))
        return error_string

class PieceIsNotOnThisBoardError(_GameError):
    def __init__(self, piece, board):
        _GameError.__init__(self)
        self.board = board

    def __str__(self):
        error_string = ("The Piece {0} is trying to move to a tile in another "
                        "board of name {1}. Pieces must be put on a board "
                        "with the Board.put_piece method before they move "
                        "there.".format(self.piece.name, self.board.name))
        return error_string

class OutOfBoardError(_GameError):
    def __init__(self, board, position):
        _GameError.__init__(self)
        self.board = board
        self.position = position

    def __str__(self):
        return ("The position {0}, {1} doesn' exist"
               "on board {2}".format(self.position.x,
                                     self.position.y,
                                     self.board))

class PositionOccupiedError(_GameError):
    def __init__(self, tile):
        _GameError.__init__(self)
        self.tile = tile

    def __str__(self):
        error_string = ("The position {0}, {1} is already "
                        " occuppied on board {2}"
                        .format(self.tile.position.x, self.tile.position.y,
                        self.tile.board.name))
        return error_string

