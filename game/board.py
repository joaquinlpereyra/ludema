from collections import namedtuple

from game.board_exceptions import OutOfBoardError, PositionOccupiedError
from game.pieces_exceptions import PieceIsNotOnThisBoardError


# this namedtuple thing is very interesting: http://goo.gl/Xs5fx5
# Pos is short for 'Position', obviously
Position = namedtuple('Position', ('x', 'y'))


class Tile:
    """A tile is the atomic unit of the Board. Every tile must have a
    board to live in. It may or may not hold a piece.
    """

    def __init__(self, board, piece=None):
        self.board = board
        self.piece = piece

    def __repr__(self):
        return ("This is the tile on map {0} holding "
                "the piece {1}".format(self.board.name, self.piece) +
                super().__repr__())

    def __str__(self):
        return self.piece.letter if self.piece else None


class Board:
    """Defines a simple square map where character can move.
    The map main attribute is the board, which is represented as a
    matrix, for example like this for a 3x3 board:
    board = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]

    On maps, all integers represent "NOTHINGNESS". All other objects
    shown on maps should be a subclass of _WorldObject.

    0: represents complete nothingness
    1: represents place where a _WorldObject _was_ but is not anymore
    2: represents place where an Item _was_ but is not anymore

    When trying to extract or set information to the board, you should
    do it like this board[y_coordinate][x_coordinate]
    """
    def __init__(self, name, size_x, size_y):
        """Initializates a simple matrix to represent the map and an
        empty dictionary of pieces in the map.
        """
        self.name = name
        self.size_x = size_x
        self.size_y = size_y
        self.board = self.__create_board()

    def __create_board(self):
        board = {}
        for x in range(self.size_x):
            for y in range(self.size_y):
                pos = Position(x, y)
                board[pos] = Tile(self)
        return board

    def __str__(self):
        """How the string will be printed.
        A . (dot) for integers, represeting emptiness.
        For everything else, print the letter attribute of the piece
        or item.
        """
        map_ = ""
        for position, tile in iter(sorted(self.board.items())):
            map_ += " . " if tile.piece is None else tile.piece.letter
            if position.y == self.size_y-1:
                map_ += "\n"
        return map_

    def __repr__(self):
        """Return the graphical representation of the map
        plus the classical python representation of an object.
        """
        return self.__str__() + '\n' + super().__repr__()

    def put_piece(self, piece, position):
        """Puts a piece on the board. Raises either OutOfBoardError or
        PossitionOccupiedError if that wasn't possible.
        """
        try:
            self.__try_moving_there(position)
        except (OutOfBoardError, PositionOccupiedError) as e:
            raise e

        destinity_tile = self.board[position]
        destinity_tile.piece = piece
        piece.home_board = self

    def move_piece(self, piece, new_position):
        """Moves piece to position (nex_x, new_y). Raises
        an either PositionOccupiedError or OutOfBoardError if that
        wasn't possible.
        """
        try:
            self.__put_nothingness_where_piece_is(piece)
            self.put_piece(piece, new_position)
        except (OutOfBoardError, PositionOccupiedError):
            raise
        except PieceIsNotOnThisBoardError:
            raise

    def remove_piece(self, piece):
        """Removes an object from the map given its position.
        Of course, we cannot remove nothingness from the map.
        Returns the (x,y) coordinates where the piece was located.
        """

        if piece.home_board is not self:
            raise PieceIsNotOnThisBoardError(piece=piece, board=self)

        self.pieces.pop(piece)
        self.__put_nothingness_where_piece_was(piece)

        return piece.position_x, piece.position_y

    def _is_valid_position(self, pos_x, pos_y):
        """Returns True if the position is found inside the map,
        False if not."""
        try:
            self.__check_position_inside_map(pos_x, pos_y)
            valid_position = True
        except OutOfBoardError:
            valid_position = False
        return valid_position

    def __put_nothingness_where_piece_is(self, piece):
        """The board has a backend value consisting of integer where
        nothingness is found. This method puts the corresponding
        integer value of nothingness in the piece position.
        Be very careful when using this: only if you're removing a piece
        or moving one.
        """
        try:
            self.tiles[piece.position].piece = None
        except KeyError:
            raise PieceIsNotOnThisBoardError(piece, self)

    def __try_moving_there(self, position):
        """Raises either a OutOfBoardError or a PositionOccupiedError
        if the position given is out of the board or occupied."""
        conditions = (self.__check_position_inside_map,
                      self.__check_position_occupied)

        for condition in conditions:
            try:
                condition(position)
            except (OutOfBoardError, PositionOccupiedError) as e:
                raise e

    def __check_position_inside_map(self, position):
        """Return True if a given position is found within the limits
        of the board.  """
        if len(self.board) < position.y and len(self.board[pos_y]) < pos_x:
            raise OutOfBoardError(pos_x, pos_y)

    def __check_position_occupied(self, pos_x, pos_y):
        """Return True if a given position if already occupied by other
        object.
        """
        if not isinstance(self.board[pos_y][pos_x], int):
            raise PositionOccupiedError(pos_x, pos_y)
