from game.exceptions import (PieceDoesNotHaveItemError, PieceIsNotOnATileError,
                             PieceIsNotOnThisBoardError, OutOfBoardError,
                             PositionOccupiedError)
from game.utils import Direction


class Piece:
    """Defines a Piece, which is _anything_ that can
    be represented on the map.

    Not intended to be used directly but rather should be used
    as superclass.
    """

    def __init__(self, letter: str, name: str=None, walkable: bool=False):
        """Initializes a Piece with a given name, letter and its home tile
        on None. The home tile should only be set by assigning the piece
        to a tile.

        args:
        name: string, the name of the piece ("John", "Door1", etc)
        letter: string, len(string) == 1, representation of piece on board
        """
        self.name = name
        self.letter = "{0}".format(letter)
        self.walkable = walkable
        self.__home_tile = None

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
        """If object has a home_tile, return a dictionary with like
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
        """
        pass

class MovablePiece(Piece):

    class Movements:
        def __init__(self, piece, movement_functions=None):
            if movement_functions is None:
                self.__default_movements(piece)
            else:
                self.__set_movements(movement_functions)

        def __default_movements(self, piece):
            def up(): return piece.move(piece.surroundings[Direction.UP])
            def right(): return piece.move(piece.surroundings[Direction.RIGHT])
            def down(): return piece.move(piece.surroundings[Direction.DOWN])
            def left(): return piece.move(piece.surroundings[Direction.LEFT])
            self.__set_movements([up, right, down, left])

        def __set_movements(self, movement_functions):
            for movement_function in movement_functions:
                setattr(self, movement_function.__name__, movement_function)

    def __init__(self, letter, name, movements=None, walkable=False):
        Piece.__init__(letter, name, walkable)
        self.movements = MovablePiece.Movements(self, movements)

    def __unsafe_move(self, tile):
        """Move the object in a certain direction, if it can:
        That means: unlink the piece from its current tile and link it
        to the new tile; unless there's a piece in the destiny tile already.

        Return True if could move there, False is possition was already
        ocuppied.

        Can raise a PieceIsNotOnATileError if the piece hasn't been put on a
        map prior to moving or a PieceIsNotOnThisBoardError if the piece
        you're trying to move has an associated tile in another board, not
        the one where the destinity tile is.
        """
        if not self.home_tile:
            raise PieceIsNotOnATileError
        if self.home_tile.board is not tile.board:
            raise PieceIsNotOnThisBoardError

        if tile.piece is not None:
            tile.piece.on_touch_do(touching_piece=self)
            if not tile.piece.walkable:
                return False

        self.home_tile.piece = None
        tile.piece = self
        return True

    def move(self, tile):
        if tile:
            try:
                return self.__unsafe_move(tile)
            except (PieceIsNotOnATileError, PieceIsNotOnThisBoardError):
                return False
        else:
            return False


class Wall(Piece):
    def __init__(self, letter="."):
        Piece.__init__(self, letter)


class Character(MovablePiece):
    """A baseclass for all characters, be them the Player or NPCs.
    Should not be used directly.
    """
    def __init__(self, letter, name, items=[], health=10):
        Piece.__init__(self, letter, name)
        self.letter = letter
        self.name = name
        self.items = items
        self.health = health

    @property
    def is_dead(self):
        return False if self.health else True

    def use_item(self, item):
        """Uses item _item_ on the home_map of the character. Returns
        the action specified by the item."""
        if item not in self.items:
            raise PieceDoesNotHaveItemError(self, item)
        if not self.surroundings:
            raise PieceIsNotOnATileError

        self.items.remove(item)
        action = item.do_action()
        return action

    def grab_item(self, tile_where_item_is):
        if not isinstance(tile_where_item_is.piece, Piece):
            raise NoItemToGrab

        self.items.append(tile_where_item_is.piece)
        tile_where_item_is.piece = None

    def grab_item_from_surroundings(self):
        for tile in filter(lambda i: i is not None, self.surroundings):
            try:
                grab_item(tile)
                return True
            except NoItemToGrab:
                continue
        else:
            return False


class Player(Character):
    """The Player character."""
    def __init__(self, letter, name, items=[], health=10):
        Character.__init__(self, letter, name, items, health=10)


class NPC(Character):
    def __init__(self, letter, name, items=[], health=10):
        Character.__init__(self, letter, name, items)

    def do_passive_action(self):
        pass

    def do_active_action(self):
        pass
