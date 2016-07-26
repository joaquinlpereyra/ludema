from game.board_exceptions import OutOfBoardError, PositionOccupiedError
from game.piece_exceptions import PieceIsNotOnThisBoardError
from game.items import _Item
from game.pieces import _Piece


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
    def __init__(self, size_x, size_y):
        """Initializates a simple matrix to represent the map and an
        empty dictionary of pieces in the map.
        """
        row = [0 for _ in range(size_x)]
        self.board = [row.copy() for _ in range(size_y)]
        self.pieces = {}

    def __str__(self):
        """How the string will be printed.
        A . (dot) for integers, represeting emptiness.
        For everything else, print the letter attribute of the piece
        or item.
        """
        map_ = ""
        for row in self.board:
            map_ += "."
            for place in row:
                if place in self.pieces:
                    map_ += place.letter
                else:
                    map_ += "  "
            map_ += ". \n"
        return map_

    def __repr__(self):
        """Return the graphical representation of the map
        plus the classical python representation of an object.
        """
        return self.__str__() + '\n' + super().__repr__()

    def put_piece(self, piece, pos_x, pos_y):
        """Puts a piece on the board. Raises either OutOfBoardError or
        PossitionOccupiedError if that wasn't possible.
        """
        try:
            self.__try_moving_there(pos_x, pos_y)
        except (OutOfBoardError, PositionOccupiedError) as e:
            raise e

        self.board[pos_y][pos_x] = piece
        self.pieces[piece] = (pos_x, pos_y)
        piece.home_board = self

    def move_piece(self, piece, new_x, new_y):
        """Moves piece to position (nex_x, new_y). Raises
        an either PositionOccupiedError or OutOfBoardError if that
        wasn't possible.
        """
        try:
            old_pos_x, old_pos_y = piece.position_x, piece.position_y
            self.pieces[piece] = (new_x, new_y)
            self.__put_nothingness_where_piece_was(piece)
            self.put_piece(piece, new_x, new_y)
        except (OutOfBoardError, PositionOccupiedError):
            raise
        except KeyError:
            raise PieceIsNotOnThisBoardError(piece, self)

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

    def __put_nothingness_where_piece_was(self, piece):
        """The board has a backend value consisting of integer where
        nothingness is found. This method puts the corresponding
        integer value of nothingness in the piece position.
        Be very careful when using this: only if you're removing a piece
        or moving one.
        """
        piece_pos_x, piece_pos_y = piece.position_x, piece.position_y
        if isinstance(piece, _Piece):
            self.board[piece_pos_y][piece_pos_x] = 1
        elif isinstance(piece, _Item):
            self.board[piece_pos_y][piece_pos_x] = 2

        return self.board[piece_pos_y][piece_pos_x]

    def __try_moving_there(self, pos_x, pos_y):
        """Raises either a OutOfBoardError or a PositionOccupiedError
        if the position given is out of the board or occupied."""
        conditions = (self.__check_position_inside_map,
                      self.__check_position_occupied)

        for condition in conditions:
            try:
                condition(pos_x, pos_y)
            except (OutOfBoardError, PositionOccupiedError) as e:
                raise e

    def __check_position_inside_map(self, pos_x, pos_y):
        """Return True if a given position is found within the limits
        of the board.  """
        if len(self.board) < pos_y and len(self.board[pos_y]) < pos_x:
            raise OutOfBoardError(pos_x, pos_y)

    def __check_position_occupied(self, pos_x, pos_y):
        """Return True if a given position if already occupied by other
        object.
        """
        if not isinstance(self.board[pos_y][pos_x], int):
            raise PositionOccupiedError(pos_x, pos_y)
