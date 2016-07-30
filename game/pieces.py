from game.board_exceptions import OutOfBoardError, PositionOccupiedError
from game.pieces_exceptions import CharacterDoesNotHaveItemError
from game.pieces_exceptions import CharacterIsNotOnABoardError

class _Piece:
    """Defines a Piece, which is _anything_ that can
    be represented on the map.

    Not intended to be used directly but rather should be used
    as superclass.
    """

    def __init__(self):
        """Initializates an object with a given position
        and its associated map startin on None.
        """
        self.home_board = None

    @property
    def position_x(self):
        if self.home_board is not None:
            return self.home_board.pieces[self][0]
        else:
            raise CharacterIsNotOnABoardError

    @property
    def position_y(self):
        if self.home_board is not None:
            return self.home_board.pieces[self][1]
        else:
            raise CharacterIsNotOnABoardError

    @property
    def surroundings(self):
        """If object has a home_map, return a list of 4 elems which surround
        the _WorldObject. Position of elements is clockwise:
        Up, Right, Down, Right. Sample output:
        [0, Key, Door, 2]
        That'd correspond to this view on the map.
              0
        2 OBJECT Key
             DOOR

        If _WorldObject is on the side of the board and there's nothing
        at "Left", that position will be filled with None.

        If object doesn't have a home_map the function will return None
        """
        if self.home_board is None:
            raise CharacterIsNotOnABoardError(self)

        adjacent = {"right": (self.position_x + 1, self.position_y),
                    "left": (self.position_x - 1, self.position_y),
                    "up": (self.position_x, self.position_y - 1),
                    "down": (self.position_x, self.position_y - 1)}

        map_ = self.home_board.board
        surroundings = []
        for position in adjacent.values():
            if self.home_board._is_valid_position(position[0], position[1]):
                surroundings.append(map_[position[0]][position[1]])
            else:
                surroundings.append(None)

        return surroundings

    def move(self, direction):
        """Move the object in a certain direction.
        If the object has an associated map, move the object there too.
        Return the new position of the piece as an (x,y) tuple.

        Direction must be a string equal to "up", "down", "left" or "right".
        """

        # XXX: fix duplicated dictionary
        adjacent = {"right": (self.position_x + 1, self.position_y),
                    "left": (self.position_x - 1, self.position_y),
                    "up": (self.position_x, self.position_y - 1),
                    "down": (self.position_x, self.position_y - 1)}

        new_pos_x, new_pos_y = adjacent[direction]

        if self.home_board:
            try:
                self.home_board.move_piece(self, new_pos_x, new_pos_y)
            except (OutOfBoardError, PositionOccupiedError):
                raise

        return self.position_x, self.position_y


class Door(_Piece):
    """A simple door."""
    def __init__(self, is_open=False):
        _Piece.__init__(self)
        self.letter = " D* " if is_open else " D "
        self.is_open = is_open


class _Character(_Piece):
    """A baseclass for all characters, be them the Player or NPCs.
    Should not be used directly.
    """
    def __init__(self, name, items=[]):
        _Piece.__init__(self)
        self.letter = " \u03A8 "  # 'Ψ'
        self.name = name
        self.items = items

    def use_item(self, item):
        """Uses item _item_ on the home_map of the character. Returns
        the action specified by the item."""
        if item not in self.items:
            raise CharacterDoesNotHaveItemError

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
