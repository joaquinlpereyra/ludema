from colorama import Style
from ludema.abstract.actions import Moving, Attacking, Grabbing
from ludema.exceptions import PieceIsNotOnATileError

class Piece:

    def __init__(self, letter, name=None, walkable=False, movements=None,
                 attacks=None, health=-1, turn_increasing_actions=None):
        """Defines a Piece, which is _anything_ that can
        be represented on the map.

        Note:
            Not intended to be used directly but rather should be used
            as superclass.

        The pieces have a Moving, Attacking and Grabbing interface. More information
        about the interfaces is to be found in their documentation. Suffice
        it to say that pieces act through them. There's more
        info on how in the argument section and on the documentation of the
        respective interfaces. The Moving interface is asigned to the
        Piece.move variable, and Attacking to Piece.attack, the Grabbing
        to Piece.grab, and so on.For example usage, see the bottom of this docstring.

        Note:
            Pieces can always grab from the same places they can move to.

        Args:
            letter (str): representation of piece on board. Should be of length 1
            name (str): Name of the piece. Leave None for anonymous.
            walkable (bool): Can the piece be walked over by other pieces?
            movements ([nullary functions] | None | []): movements is the parameter
                which will specify how the interface exposing the valid movements
                for the piece will be created. Give a list of nullary functions
                to specify your own movements functions, None to let the piece
                have the default movements (up, down, right, left a tile) or
                pass an empty list to explicity set NO movement functions for the piece.
                Even if you set no movement functions for the piece, you'll still
                have access to Moving.to_tile and Moving._unsafe_to_tile to manually
                specify movements if you need to do so, but you should not use them
                for normal I/O (specially not Moving._unsafe_to_tile).
                You can also safely call self.move.random and
                self.move.random_and_valid, but they won't produce a movement.

                Defaults movements:
                    Moving.up(), Moving.right(), Moving.left(), Moving.down()

            attacks ([nullary function] | None | []): Defaults to None.
                Exactly the same as movements, but for attacks. Default attacks
                (those set when the attacks parameter is None) are up, down,
                left,right a tile, with a base damage of 1.

                Default attacks:
                    Attacking.up(), Attacking.right(), Attacking.left(), Attacking.down()

            health (int): how much Health Points should this piece have?
                any negative number means "infinite health"

        Example:
            ::
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
        self.letter = "{0}{1}".format(letter, Style.RESET_ALL)
        self.walkable = walkable
        self.__home_tile = None
        self.health = health
        self.move = Moving(self, movements)
        self.attack = Attacking(self, attacks)
        self.grab = Grabbing(self, movements)  # grab from same place they can move to

    @property
    def home_tile(self):
        """TThe tile where this piece belongs."""
        return self.__home_tile

    @home_tile.setter
    def home_tile(self, home_tile):
        self.__home_tile = home_tile

    @property
    def position(self):
        """Return the position of the piece.

        Raises:
            PieceIsNotOnATileError if piece is not on a tile.
        """
        if self.home_tile is not None:
            return self.home_tile.position
        else:
            raise PieceIsNotOnATileError(self)

    @property
    def surroundings(self):
        """If object has a home_tile, return a dictionary that looks like
        {Direction : Tile or None} for each of the four cardinal directions.
        Value will be None if the direction is outside the map.

        Raises:
            PieceIsNotOnAtile if its home_tile is None.
        """

        if self.home_tile is None:
            raise PieceIsNotOnATileError(self)

        board = self.home_tile.board
        surroundings = board.get_adjacent_to_tile(self.home_tile)

        return surroundings

    def on_touch_do(self, touching_piece):
        """What should the piece do when it is touched by another piece?
        IE: when a piece tries to move to the position this one occupies.

        Args:
            touching_piece (Piece): the piece that touches this one
        """
        pass
