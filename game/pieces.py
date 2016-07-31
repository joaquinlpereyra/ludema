from game.exceptions import (PieceDoesNotHaveItemError, PieceIsNotOnATileError,
                             PieceIsNotOnThisBoardError, OutOfBoardError,
                             PositionOccupiedError)


class _Piece:
    """Defines a Piece, which is _anything_ that can
    be represented on the map.

    Not intended to be used directly but rather should be used
    as superclass.
    """

    def __init__(self, name):
        """Initializates an object with a given position
        and its associated map startin on None.
        """
        self.name = name

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


class Door(_Piece):
    """A simple door."""
    def __init__(self, name, is_open=False):
        _Piece.__init__(self, name)
        self.letter = " D* " if is_open else " D "
        self.is_open = is_open


class _Character(_Piece):
    """A baseclass for all characters, be them the Player or NPCs.
    Should not be used directly.
    """
    def __init__(self, name, items=[]):
        _Piece.__init__(self, name)
        self.letter = " \u03A8 "  # 'Ψ'
        self.name = name
        self.items = items

    def use_item(self, item):
        """Uses item _item_ on the home_map of the character. Returns
        the action specified by the item."""
        if item not in self.items:
            raise PieceDoesNotHaveItemError

        self.items.remove(item)
        action = item.do_action(self.home_map)
        return action


class Player(_Character):
    """The Player character."""
    # TODO: IMPLEMENT
    pass


class NPC(_Character):
    """A non-playable character."""
    # TODO: implement
    pass
