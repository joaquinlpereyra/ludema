class _GameError(Exception):
    """Baseclass for all exceptions."""
    def __init__(self):
        pass

class CharacterCantAttackError(_GameError):
    def __init__(self, character):
        _GameError.__init__(self)
        self.character = character

    def __str__(self):
        error_string = ("The Character {0} doesn't have an attack_damage "
                        "value and thus cannot attack.".format(self.character))
        return error_string

class TurnCanOnlyBeIncreased(_GameError):
    def __init__(self, prev_turn, new_turn):
        _GameError.__init__(self)
        self.prev_turn = prev_turn
        self.new_turn = new_turn

    def __str__(self):
        error_string = ("Someone tried to set the turn to {0} but the "
                        "turn was already {1}. You can't go back in time "
                        "(at least not in turns)".format(self.new_turn,
                        self.prev_turn))
        return error_string

class TurnsAreOver(_GameError):
    def __init__(self, board):
        _GameError.__init__(self)
        self.board = board

    def __str__(self):
        error_string = ("Turns are over on board {0}".format(self.board.name))
        return error_string

class TileIsEmptyError(_GameError):
    def __init__(self, character, tile, error_string=None):
        _GameError.__init__(self)
        self.character = character
        self.tile = tile
        self.error_string = error_string

    def __str__(self):
        if not self.error_string:
            self.error_string = ("The Character {0} tried to attack tile {1}, "
                                 "but that tile does not have a character."
                                 .format(self.character, self.tile))
        return error_string

class NotGrabbableError(_GameError):
    def __init__(self, character, tile, error_string=None):
        _GameError.__init__(self)
        self.piece = piece

    def __str__(self):
        return "The piece {0} doesn't implement the grab method".format(self.piece)

class NoItemToGrab(_GameError):
    def __init__(self, character):
        self.character = character

    def __str__(self):
        error_string = ("The Character {0} tried to grab an item, "
                        "but no item was found.".format(self.character))

class PieceDoesNotHaveItemError(_GameError):
    def __init__(self, piece, item):
        _GameError.__init__(self)
        self.piece = piece
        self.item = item

    def __str__(self):
        error_string = ("The Piece {0} doesn't have item {1}"
                        .format(self.piece.name, self.item.name))
        return error_string

class BoardError(_GameError):
    def __init__(self):
        _GameError.__init__(self)

class PieceIsNotOnATileError(BoardError):
    def __init__(self, piece):
        BoardError.__init__(self)
        self.piece = piece

    def __str__(self):
        error_string = ("The Piece {0} isn't on a tile. Pieces must be "
                        "put on a tile the Board.put_piece method "
                        "before they can perform actions.".format(self.piece.name))
        return error_string

class PieceIsNotOnThisBoardError(BoardError):
    def __init__(self, piece, board):
        BoardError.__init__(self)
        self.board = board

    def __str__(self):
        error_string = ("The Piece {0} is trying to move to a tile in another "
                        "board of name {1}. Pieces must be put on a board "
                        "with the Board.put_piece method before they move "
                        "there.".format(self.piece.name, self.board.name))
        return error_string

class OutOfBoardError(BoardError):
    def __init__(self, board, position):
        BoardError.__init__(self)
        self.board = board
        self.position = position

    def __str__(self):
        return ("The position {0}, {1} doesn' exist"
               "on board {2}".format(self.position.x,
                                     self.position.y,
                                     self.board))

class PositionOccupiedError(BoardError):
    def __init__(self, tile):
        BoardError.__init__(self)
        self.tile = tile

    def __str__(self):
        error_string = ("The position {0}, {1} is already "
                        " occuppied on board {2}"
                        .format(self.tile.position.x, self.tile.position.y,
                        self.tile.board.name))
        return error_string

class BoardConstructionError(BoardError):
    def __init__(self):
        BoardError.__init__(self)

class WrongSizeOnY(BoardConstructionError):
    def __init__(self):
        BoardConstructionError.__init__(self)

    def __str__(self):
        return ("The amount of lines on your constructor string does not match "
                "the height of your board.")

class WrongSizeOnX(BoardConstructionError):
    def __init__(self):
        BoardConstructionError.__init__(self)

    def __str__(self):
        return ("The lentgh of one or more of the lines on your constructor "
                "string does not match the width of your board.")

class RowsOfDifferentSizes(BoardConstructionError):
    def __init__(self):
        BoardConstructionError.__init__(self)

    def __str__(self):
        return ("The length of the lines on your constructor string "
                "do not match. The board has to be a rectangle.")

class ImpossibleToExtractPiece(BoardConstructionError):
    def __init__(self, container):
        BoardConstructionError.__init__(self)
        self.container = container

    def __str__(self):
        return ("I can't sensibly extract a piece from this container: {0}".format(container))
