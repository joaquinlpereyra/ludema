from ludema.abstract.actions import Moving, Attacking

class Piece:
    """Defines a Piece, which is _anything_ that can
    be represented on the map.

    Not intended to be used directly but rather should be used
    as superclass.
    """

    def __init__(self, letter, name=None, walkable=False, movements=None,
                 attacks=None):
        """Initializes a Piece with a given name, letter and its home tile
        on None. The home tile should only be set by assigning the piece
        to a tile.

        The pieces have a Moving and an Attacking interface. More information
        about the interfaces is to be found in their documentation. Suffice
        it to say that pieces move and attack through them. There's more
        info on how in the @args section and on the documentation of the
        respective interfaces. The Moving interface is asigned to the
        Piece.move variable, and Attacking to Piece.attack. For example
        usage, see the bottom of this docstring.

        @args:
        letter (string) [len(string) == 1]: representation of piece on board
        name (string | None): Defaults to None. Name of the piece. Leave None
            for anonymous.
        walkable (bool): Defaults to False. Can the piece be walked over by
            other pieces?
        movements ([nullary functions] | None | []): Defaults to None.
            movements is the parameter which will specify how the interface
            exposing the valid movements for the piece will be created. Give a
            list of nullary functions to specify youw own movements functions,
            None to let the piece have the default movements
            (up, down, right, left a tile) or pass an empty list to explicity
            set NO movement functions for the piece.  Even if you set
            no movement functions for the piece, you'll still have access
            to Moving.to_tile and Moving._unsafe_to_tile to manually specify
            movements if you need to do so, but you should not use them
            for normal I/O (specially not Moving._unsafe_to_tile).
            You can also safely call self.move.random and
            self.move.random_and_valid, but they won't produce a movement.

            Defaults movements: Moving.up(), Moving.right(), Moving.left(),
                                Moving.down()
        attacks ([nullary function] | None | []): Defaults to None.
            Exactly the same as movements, but for attacks. Default attacks
            (those set when the attacks parameter is None) are up, down,
            left,right a tile, with a base damage of 1.

            Default attacks: Attacking.up(), Attacking.right(),
                             Attacking.left(), Attacking.down()

        @examples:
        first_level = Board(name="First Level", size_x=10, size_y=10)

        bruma = Piece("@", "Bruma")
        first_level.put_piece(bruma, Position(1,1))
        a_piece.move.up()  # will move the piece up a tile
        a_piece.attack.left()  # will attack the tile at left of the piece

        grass = Piece("*", walkable=True, movements=[], attacks=[])
        first_level.put_piece(grass, Position(3,3))
        grass_piece.move.to_tile(first_level.board[2,2])
        grass_piece.move.up()  # error: method doesn't exist
        """
        self.name = name
        self.letter = "{0}".format(letter)
        self.walkable = walkable
        self.__home_tile = None
        self.move = Moving(self, movements)
        #self.attack = Attacking(attacks)

    @property
    def home_tile(self):
        return self.__home_tile

    @home_tile.setter
    def home_tile(self, home_tile):
        self.__home_tile = home_tile

    @property
    def position(self):
        if self.home_tile is not None:
            return self.home_tile.position
        else:
            raise PieceIsNotOnATileError(self)

    @property
    def surroundings(self):
        """If object has a home_tile, return a dictionary that looks like
        {Direction : Tile or None} for each of the four cardinal directions.
        Value will be None if the direction is outside the map.

        Will raise an CharacterIsNotOnATileError if self.home_tile is None.
        """

        if self.home_tile is None:
            raise PieceIsNotOnATileError(self)

        board = self.home_tile.board
        surroundings = board.get_adjacent_to_tile(self.home_tile)

        return surroundings

    def on_touch_do(self, touching_piece):
        """What should the piece do when it is touched by another piece?
        IE: when a piece tries to move to the position this one occupies.

        @args:
        touching_piece (Piece): the piece that touches this one
        """
        raise NotImplementedError("Piece should'n be used directly!")
