from ludema import pieces
from ludema import utils
from ludema.abstract.utils import Position, Direction
from ludema.abstract.piece import Piece
from ludema.exceptions import (PieceIsNotOnThisBoardError, OutOfBoardError,
                               PositionOccupiedError, TurnCanOnlyBeIncreased,
                               TurnsAreOver, WrongSizeOnX, WrongSizeOnY,
                               RowsOfDifferentSizes)

"""
The purpose of this module is to define a board where the pieces can move.
The majority of this work is carried of by the Board class, but the
Tile is also quite important.
"""




class Board:
    """Defines a simple rectangular map where the Pieces interact.  """
    @classmethod
    def new_from_blueprint(cls, name, blueprint, legend, win_conditions,
                           lose_conditions, empty_repr = "   ", turn_limit=-1):
        """An alternative creator for Board, which uses Board.fill_board_with_blueprint
        inmediatly after creation to create a board according to a blueprint
        and a legend. Refer to documentation for that method for more information.

        Args:
            name (str): the name of the board
            blueprint (str): the blueprint for the board
            legend ({key: (Piece | [Piece] | (nullary function -> Piece}): legend
                for the blueprint
            win_conditions ([nullary functions]): each turn will be evaluated, if
                ONE returns True, the board is WON
            lose_condtitions ([nullary functions]): idem win_conditions, but if ONE
                returns True, the board is considered lost
            empty_repr (str): what should an empty espace be represented as?
            turn_limit: (int): if turn limit is passed, raise TurnsAreOver error.
                any negative number will be interpreted as no turn limit.
        """

        blueprint = blueprint.replace(" ", "")
        lines = blueprint.split('\n')[1:-1]
        board = cls(name, len(lines[0]), len(lines), win_conditions, lose_conditions, empty_repr, turn_limit)
        board.fill_board_with_blueprint(blueprint, legend)
        return board

    def __init__(self, name, size_x, size_y, win_conditions, lose_conditions,
                 empty_repr="   ", turn_limit=-1):
        """
        Args:
            name (str): the name of the board
            size_x (int): the horizontal size of the board
            size_y (int): the vertical size of the board
            win_conditions ([nullary functions]): each turn will be evaluated, if
                ONE returns True, the board is WON
            lose_condtitions ([nullary functions]): idem win_conditions, but if ONE
                returns True, the board is considered lost
            empty_repr (str): what should an empty espace be represented as?.
            turn_limit: (int): if turn limit is passed, raise TurnsAreOver error.
                any negative number will be interpreted as no turn limit.

        See also:
            :func:`~ludema.board.Board.new_from_blueprint`: alternative contructor for a Board.
        """

        self.name = name
        self.win_conditions = win_conditions
        self.lose_conditions = lose_conditions
        self.size_x = size_x
        self.size_y = size_y
        self.empty_repr = empty_repr
        self.board = self.__create_board(size_x, size_y)
        self.players = []
        self.npcs = []  # non playable characters
        self.turn_limit = turn_limit
        self._turn = 0

    @property
    def won(self):
        """This property will return wether the board has been won or not.
        Has no setter.
        """
        return any([win_condition() for win_condition in self.win_conditions])

    @property
    def lost(self):
        """This property will return wether the board has been lost or not.
        Has no setter.
        """
        return any([lose_condition() for lose_condition in self.lose_conditions])

    @property
    def turn(self):
        """This property defines the turns passed on the board.
        You can increment it as you wish, but you can never decrement it.
        """
        return self._turn

    @turn.setter
    def turn(self, new_turn):
        if new_turn <= self.turn:
            raise TurnCanOnlyBeIncreased(self.turn, new_turn)
        turns_passed = new_turn - self._turn  # in most cases this should be 1
        for _ in range(turns_passed):
            for character in (self.npcs + self.players):
                character.do_passive_action()
        self._turn = new_turn
        if self.turn_limit > 0 and self._turn > self.turn_limit:
            raise TurnsAreOver(self)

    def __create_board(self, size_x, size_y):
        """Fill board with empty tiles.

        Args:
            size_x: width of board
            size_y: height of board
        """
        board = []
        for x in range(size_x):
            board.append([Tile(self, Position(x, y)) for y in range(size_y)])
        return board

    def __str__(self):
        """How the board will represented as a string."""

        # NOTE: this is quite the mess so don' touch unless you know
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
                name_length = len(str(tile))
                if not str(tile):
                    map_ += self.empty_repr
                elif name_length == 1:
                    map_ +=  " {0} ".format(str(tile))
                elif name_length == 2:
                    map_ += " {0}".format(str(tile))
                elif name_length == 3:
                    map_ += "{0}".format(str(tile))
                else:
                    map_ += " {0} ".format(str(tile))

            map_ += "\n"
        return map_

    def __repr__(self):
        """Return the graphical representation of the map
        plus the classical python representation of an object.
        """
        return (str(self.board) + '\n ' +
                ' Board Name: ' + self.name + '|' + super().__repr__())

    def fill_board_with_blueprint(self, blueprint, legend):
        """Take a blueprint and a legend for it and fill the board
        according to them.

        The blueprint string ignores blank spaces and automatically ignores
        the first and last lines of the string. That is to allow for this
        very convenient format: ::

            blueprint = \"\"\"
            . . . . . .
            . * * * * .
            . * @ . * .
            . * * * * .
            . . . . . .
            \"\"\"

        Args:
            blueprint (str): a string representing the board, example given above
            legend ({letter: (Piece | [Piece] | nullary function -> Piece): a dictionary
                that maps from characters found on the blueprint to which piece
                should be put in the place specified by the blueprint.
                if legend[letter] is a list, the last element of the list will be
                put first (scanning from the top lefmost corner and continuing
                to the right and then belown).
                if legend[letter] is a nularry function that returns a Piece,
                the piece returned by the nulary function will be put in place

        Raises:
            WrongeSizeOnX: if the blueprint doesn't have the correct width
            WrongSizeOnY: if the blueprint doesn't have correct height
            RowsOfDifferentSizes: if the blueprint isn't rectangular
            ImpossibleToExtractPiece: if something weird happened when
                trying to excract a Piece from the legend

        Example:

            Defining a blueprint and a legend is simple. The following should
            be clear enough.::

                blueprint = \"\"\"
                . . . . . .
                . * * * * .
                . * @ . * .
                . * * * * .
                . . . . . .
                \"\"\"
                lengend = {'*': Wall,
                           '@': myCharacter}
                my_board.fill_board_with_blueprint(blueprint, legend)
        """

        # NOTE: this creates a copy of the lists in the dict, because
        # extract_pieces_from_possible_containers modfies a potential list
        # this dictionary holds as a value, leading to some very unfortunate
        # and hard to trace bugs
        legend = utils.copy_lists_in_dictionary(legend)

        blueprint = blueprint.replace(" ", "")
        lines = blueprint.split('\n')[1:-1]

        if len(lines) != self.size_y:
            raise WrongSizeOnY
        if len(lines[0]) != self.size_x:
            raise WrongSizeOnX
        if not all([len(line) == len(lines[0]) for line in lines]):
            raise RowsOfDifferentSizes

        for y_position, string in enumerate(reversed(lines)):
            for x_position, letter in enumerate(string):
                if letter in legend:
                    piece = utils.extract_pieces_from_possible_containers(legend[letter])
                    self.put_piece(piece, x_position, y_position)

    def put_piece(self, piece, x, y):
        """Puts a piece on the board.

        Args:
            piece (Piece): the piece which shall be put into the board
            x (int): The x coordinate where to put the piece.
            y (int): the y coordinate where to put the piece.

        Raises:
            OutOfBoardError: if (x,y) coordinates are not on board
            PositionOccupiedError: if position on (x,y) is already occupied and
                that tile is not walkable
        """

        position = Position(x, y)
        try:
            self.__try_moving_there(position)
        except (OutOfBoardError, PositionOccupiedError):
            raise

        # NOTE: This is THE ONLY PLACE where we create the bidirectional, 1 to 1
        # relationship between a tile and a piece.
        destinity_tile = self.board[position.x][position.y]
        destinity_tile.piece = piece

        if isinstance(piece, pieces.NPC):
            self.npcs.append(piece)
        elif isinstance(piece, pieces.Player):
            self.players.append(piece)

    def put_piece_on_column(self, piece_constructor, x, ranges):
        """Puts pieces returned by piece_constructor on the column
        of position X.

        If no ranges are specified, the whole row will be filled.

        Args:
            piece_constructor (nullary function): a function that returns the piece
            x (int): the x position of the column
            ranges (*tuples): arbitrary amout of ranges to put the piece on the column
        """
        if not ranges:
            ranges = [(0, self.size_y)]

        for begin, end in ranges:
            for y in range(begin, end):
                self.put_piece(piece_constructor(), x, y)

    def put_piece_on_row(self, piece_constructor, y, ranges):
        """Puts pieces returned by piece_constructor on the row of position Y.

        If no ranges are specified, the whole row will be filled.

        Args:
            piece_constructor (nullary function): a function that returns the piece
            y (int): the y position of the column
            ranges (*tuples): arbitrary amout of ranges to put the piece on the row
        """
        if not ranges:
            ranges = [(0, self.size_y)]

        for begin, end in ranges:
            for x in range(begin, end):
                self.put_piece(piece_constructor(), x, y)

    def remove_piece(self, piece):
        """Removes an object from the map given its position.
        Returns the (x,y) coordinates where the piece was located.

        Args:
            piece (Piece): the piece which will be removed

        Returns:
            (int, int): the cordinates from where the piece was removed

        Raises:
            PieceIsNotOnThisBoardError: if the piece.home_board is not this one
        """

        if piece.home_board is not self:
            raise PieceIsNotOnThisBoardError(piece=piece, board=self)

        self.put_piece(None, piece.position_x, piece.position_y)

        return piece.position_x, piece.position_y

    def get_adjacent_to_tile(self, tile):
        """Return a dictionary of the form {DIRECTION: TILE or None}.
        None will be the value only if the direction is outside of the map for
        the requested center tile.

        Args:
            tile (Tile): the 'center' tile, which surroundings we're looking for

        Returns:
            {Direction: Tile | None}: surroundings of the tile given as parameter
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

    def column_on_position(self, x):
        """Yields the tiles on column in position x.

        Args:
            x (int): the column which tiles we want to get

        Yields:
            The tiles on column x.
        """
        for y in range(self.size_y):
            yield self.board[x][y]

    def row_on_postition(self, y):
        """Yields the tiles on row in position y.

        Args:
            y (int): the row which tiles we want to get

        Yields:
            The tiles on row y.
        """
        for x in range(self.size_x):
            yield self.board[x][y]

    def _is_valid_position(self, position):
        """
        Args:
            position (Position): the position which we are interested in

        Returns:
            True if position inside the map, False if not
        """
        try:
            self.__check_position_inside_map(position)
            valid_position = True
        except OutOfBoardError:
            valid_position = False
        return valid_position

    def __try_moving_there(self, position):
        """Raises either a OutOfBoardError or a PositionOccupiedError
        if the position given is out of the board or occupied.

        Args:
            position (Position): the position which we are insterested in

        Raises:
            OutOfBoardError: if the position is outside of this board
            PositionOccupiedError: if the posision is already occupied
        """
        conditions = (self.__check_position_inside_map,
                      self.__check_position_occupied)

        for condition in conditions:
            try:
                condition(position)
            except (OutOfBoardError, PositionOccupiedError) as e:
                raise e

    def __check_position_inside_map(self, position):
        """Return True if a given position is found within the limits
        of the board.

        Args:
            position (Position): the position to check

        Raises:
            OutOfBoardError: if posisition is out of this board
        """
        x_pos, y_pos = abs(position.x), abs(position.y)
        if self.size_y <= y_pos or self.size_x <= x_pos:
            raise OutOfBoardError(self, position)

    def __check_position_occupied(self, position):
        """Return True if a given position if already occupied by other
        object.

        Args:
            position (Position): the position to check

        Raises:
            PositionOccupiedError: if posisition is already occupied
        """
        tile = self.board[position.x][position.y]
        if tile.piece is not None and not tile.piece.walkable:
            raise PositionOccupiedError(tile)


class Tile:
    """A tile is the atomic unit of the Board.
    """
    def __init__(self, board, position, piece=None):
        """
        Every tile lives on a board and has a position there.
        A tile may or may not hold a piece.

        Args:
            board (Board): the board where the tile lives.
            position (Position): the position of this tile.
            piece (Piece or None): the piece present on this tile.

        Note:
            You most probably don't want to create a Tile. Boards manage and
            create tiles by themselves when they are created.
        """
        self.board = board
        self.position = position
        self._piece_stack = [piece]

    @property
    def piece(self):
        """The piece property returns the topmost piece on a tile (as tiles
        may hold several pieces).

        Setting the tile's piece to None will **remove** and
        return the topmost piece.
        """
        return self._piece_stack[-1]

    @piece.setter
    def piece(self, piece):
        # if we currently have no piece or it is walkable, just change the topmost
        if self.piece is None or self.piece.walkable:
            self._piece_stack.append(piece)
            piece.home_tile = self
        # we interpret the 'None' type as removing a piece from the tile
        if piece is None:
            self._piece_stack.pop()

    def __repr__(self):
        original = super().__repr__()
        custom = " at {0} on map {1} holding {2}".format(self.position,
                                                         self.board.name,
                                                         self.piece)
        return original + custom

    def __str__(self):
        return self.piece.letter if self.piece else ""
