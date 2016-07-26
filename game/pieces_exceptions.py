class _PieceError(Exception):
    def __init__(self, piece):
        self.piece = piece

class _CharacterError(_PieceError):
    def __init__(self, char):
        _PieceError.__init__(self, char)

class CharacterDoesNotHaveItemError(_CharacterError):
    def __init__(self, char, item):
        _CharacterError.__init__(self, char)
        self.item = item

class CharacterIsNotOnABoardError(_CharacterError):
    def __init__(self, char):
        _CharacterError.__init__(self, char)

class PieceIsNotOnThisBoardError(_PieceError):
    def __init__(self, piece, board):
        _PieceError.__init__(self, piece)
        self.board = board


