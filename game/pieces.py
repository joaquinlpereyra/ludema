from game.exceptions import (PieceDoesNotHaveItemError, PieceIsNotOnATileError,
                             PieceIsNotOnThisBoardError, OutOfBoardError,
                             PositionOccupiedError)


class Piece:
    """Defines a Piece, which is _anything_ that can
    be represented on the map.

    Not intended to be used directly but rather should be used
    as superclass.
    """

    def __init__(self, name, letter):
        """Initializes a Piece with a given name, letter and its home tile
        on None. The home tile should only be set by assigning the piece
        to a tile.

        args:
        name: string, the name of the piece ("John", "Door1", etc)
        letter: string, len(string) == 1, representation of piece on board
        """
        self.name = name
        self.letter = "{0}".format(letter)
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

    def move(self, tile):
        """Move the object in a certain direction.
        That means: unlink the piece from its current tile and link it
        to the new tile.

        Raise CharacterIsNotOnATileError if piece didn't already
        have an associated tile, CharacterIsNotOnThisBoardError if
        the destinity tile is not on the same board as the current tile,
        OutOfBoard error if destinity tile is falsey (most probably
        this means you're tring to move somewhere outside the map)
        """
        if tile.piece is not None:
            raise PositionOccupiedError(tile)
        if not self.home_tile:
            raise PieceIsNotOnATileError
        if self.home_tile.board is not self.home_tile.board:
            raise PieceIsNotOnThisBoardError
        if not tile:
            raise OutOfBoardError

        self.home_tile.piece = None
        tile.piece = self


class Character(Piece):
    """A baseclass for all characters, be them the Player or NPCs.
    Should not be used directly.
    """
    def __init__(self, letter, name, items=[]):
        Piece.__init__(self, letter, name)
        # self.letter = " \u03A8 "  # 'Ψ'
        self.letter = letter
        self.items = items

    def use_item(self, item):
        """Uses item _item_ on the home_map of the character. Returns
        the action specified by the item."""
        if item not in self.items:
            raise PieceDoesNotHaveItemError
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

class Player(Character):
    """The Player character."""
    # TODO: IMPLEMENT
    pass


class NPC(Character):
    """A non-playable character."""
    # TODO: implement
    pass
