from game.utils import Position, Direction
from game.exceptions import (PieceIsNotOnThisBoardError, OutOfBoardError,
                             PositionOccupiedError)

"""
The purpose of this module is to define a board where the pieces can move.
The majority of this work is carried of by the Board class, but the
Tile is also quite important.

The Position named tuple should be self explanatory. It's usage is
MANDATORY, no reference to the position of something on the map should
be made in any other way than by using Position.
"""


class _Tile:
    """A tile is the atomic unit of the Board. Every tile must have a
    board to live in. Every tile must have a position on said board.
    A tile may or may not hold a piece.

    """
    def __init__(self, board, position, piece=None):
        self.board = board
        self.position = position
        self.__piece = piece

    @property
    def piece(self):
        return self.__piece

    @piece.setter
    def piece(self, piece):
        if piece is not None:
            piece.home_tile = self
        self.__piece = piece

    def __repr__(self):
        original = super().__repr__()
        custom = " at {0} on map {1} holding {2}".format(self.position,
                                                         self.board.name,
                                                         self.piece)
        return original + custom

    def __str__(self):
        return self.piece.letter if self.piece else "."


class Board:
    """Defines a simple square board where Pieces can move.
    The board's main attribute is the board itself, which is a matrix of the
    form (for a 2x3 board):
    board = [[Tile(self, Position(0, 0)], Tile(self, Position(0, 1))]
             [Tile(self, Position(1, 0))], Tile(self, Position(1, 1))],
             [Tile(self, Position(2, 0))], Tile(self, Position(2, 1))]

    This structure was chosen so you could so board[x][y] and get a meaningful
    result.

    Note that the last two arguments of the Tile are actually ony one
    Postition namedtuple.
    """
    def __init__(self, name, size_x, size_y):
        """Initializes the object with a name and a board."""
        self.name = name
        self.size_x = size_x
        self.size_y = size_y
        self.board = self.__create_board(size_x, size_y)

    def __create_board(self, size_x, size_y):
        """Return a board as described in the docstring of the class."""
        board = []
        for x in range(size_x):
            board.append([_Tile(self, Position(x, y)) for y in range(size_y)])
        return board

    def __str__(self):
        """How the board will represented as a string."""

        # NOTE: this is quite the mess so don' touch unless you know what
        # what you're doing

        def board_from_column_to_rows():
            """Our board is a list of COLUMNS. Return a list of ROWS."""
            rows = []
            # range is reversed so as to start printing from the topmost row
            for y in reversed(range(self.size_y)):
                row = [self.board[x][y] for x in range(self.size_x)]
                rows.append(row)
            return rows

        map_ = ""
        rows = board_from_column_to_rows()
        for row in rows:
            for tile in row:
                map_ += " {0} ".format(str(tile))
            map_ += "\n"
        return map_

    def __repr__(self):
        """Return the graphical representation of the map
        plus the classical python representation of an object.
        """
        return (str(self.board) + '\n ' +
                ' Board Name: ' + self.name + '|' + super().__repr__())

    def put_piece(self, piece, position):
        """Puts a piece on the board. Raises either OutOfBoardError or
        PossitionOccupiedError if that wasn't possible.

        This is THE ONLY PLACE where we create the bidirectional relationship
        between a tile and a piece.
        """
        try:
            self.__try_moving_there(position)
        except (OutOfBoardError, PositionOccupiedError) as e:
            raise e

        destinity_tile = self.board[position.x][position.y]
        destinity_tile.piece = piece

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

    def get_adjacent_to_tile(self, tile):
        """Return a dictionary of the form {DIRECTION: TILE or None}.
        None will be the value only if the direction is outside of the map for
        the requested center tile.
        """

        position = tile.position
        ideal_adjacent = {
            Direction.UP: Position(position.x, position.y + 1),
            Direction.RIGHT: Position(position.x + 1, position.y),
            Direction.DOWN: Position(position.x, position.y - 1),
            Direction.LEFT: Position(position.x - 1,  position.y)
            }

        adjacent = {}
        for direction, position in iter(ideal_adjacent.items()):
            if self._is_valid_position(position):
                adjacent[direction] = self.board[position.x][position.y]
            else:
                adjacent[direction] = None

        return adjacent

    def _is_valid_position(self, position):
        """Returns True if the position is found inside the map,
        False if not."""
        try:
            self.__check_position_inside_map(position)
            valid_position = True
        except OutOfBoardError:
            valid_position = False
        return valid_position

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
        x_pos, y_pos = abs(position.x), abs(position.y)
        if len(self.board) <= y_pos or len(self.board[y_pos]) <= x_pos:
            raise OutOfBoardError(self, position)

    def __check_position_occupied(self, position):
        """Return True if a given position if already occupied by other
        object.
        """
        if self.board[position.x][position.y].piece is not None:
            raise PositionOccupiedError(self, position)
