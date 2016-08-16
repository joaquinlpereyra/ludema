from ludema.abstract.utils import Direction
from ludema.exceptions import PieceIsNotOnATileError, PieceIsNotOnThisBoardError
import random

class Action:
    def __init__(self, piece, action_functions):
        self.possible_actions = []
        self.piece = piece
        if action_functions is None:
            action_functions = self._default_actions()
        self._set_actions(action_functions)

    @property
    def is_implemented(self):
        return True if self.possible_actions else False

    def _normal_default_actions(self):
        def up():
            return self.do(self.piece, self.piece.surroundings[Direction.UP])
        def right():
            return self.do(self.piece, self.piece.surroundings[Direction.RIGHT])
        def down():
            return self.do(self.piece, self.piece.surroundings[Direction.DOWN])
        def left():
            return self.do(self.piece, self.piece.surroundings[Direction.LEFT])
        return [up, right, down, left]

    def _set_actions(self, action_functions):
        for action_function in action_functions:
            self.possible_actions.append(action_function)
            setattr(self, action_function.__name__, action_function)

    def _default_actions(self):
        raise NotImplementedError("The Action class shouldn't be used directly!")

    def _unsafe_do(self, tile):
        raise NotImplementedError("The Action class shouldn't be used directly!")

    def do(self, piece, tile):
        raise NotImplementedError("The Action class shouldn't be used directly!")


class Moving(Action):
    """This clase represents the 'Move' interface owned by a MovablePiece
    instance.
    It's job is to hold functions that move the MovablePiece in a direction.
    It also holds a list with all the posible movements the Piece can do,
    so you can choose one at random or inspect them dynamically.
    """
    def __init__(self, piece, movement_functions):
        """Starts the object with an empty list of possible movements and
        forces it to have at least the deafult ones.

        @args:
        piece (MovablePiece): the movable piece to which the movements refer
        movement_functions ([nullary functions]): a list of valid
            functions which as a side effect move the piece.
        """
        Action.__init__(self, piece, movement_functions)
        self.possible_movements = self.possible_actions

    def _default_actions(self):
        """Create and set the default movement functions (up, down, left,
        right)

        @args:
        piece (MovablePiece): the MovablePiece to be moved

        @return:
        None
        """
        return self._normal_default_actions()

    def _unsafe_do(self, tile):
        """Move the object if it can.
        That means: unlink the piece from its current tile and link it
        to the new tile; unless there's a piece in the destiny tile already.

        Return True if could move there, False is possition was already
        ocuppied. This method should not be used for I/O, as it can raise
        errors. Use the move_to_tile method instead.

        Can raise a PieceIsNotOnATileError if the piece hasn't been put on a
        map prior to moving or a PieceIsNotOnThisBoardError if the piece
        you're trying to move has an associated tile in another board, not
        the one where the destinity tile is.

        @args:
        tile (Tile): the tile to which the piece will try to move

        @return:
        bool: False if there was a piece on tile and it wasn't walkable,
              True if movement could be completed
        """
        if not self.piece.home_tile:
            raise PieceIsNotOnATileError
        if self.piece.home_tile.board is not tile.board:
            raise PieceIsNotOnThisBoardError

        if tile.piece is not None:
            tile.piece.on_touch_do(touching_piece=self.piece)
            if not tile.piece.walkable:
                return False

        self.piece.home_tile.piece = None
        tile.piece = self.piece
        return True

    def do(self, piece, tile):
        """Move the object, if it can.
        A safe version of _unsafe_move_to_tile, prepared for I/O. Refer to
        that method for implementation details. This method should never
        raise an error.

        Return True if piece could be moved, False if not.

        @args:
        tile (Tile): the tile to which the piece will try to move.
        """

        if tile:
            try:
                return self._unsafe_do(tile)
            except (PieceIsNotOnATileError, PieceIsNotOnThisBoardError):
                return False
        else:
            return False

    def random(self):
        """Call and return a random function from the possible movements
        list. Keep in mind that the movement may or may not be effective,
        depending on the current position of the piece and where
        the movement tries to send the piece. For a random valid movent,
        call the random_and_valid method.

        @return:
        boolean, True if movement was made, False if not
        """
        try:
            surprise_move = random.choice(self.possible_movements)
        except IndexError:
            return False
        was_movement_valid = surprise_move()
        return was_movement_valid

    def random_and_valid(self):
        """Call and return a random function from the possible movements,
        making sure that the movement is actually possible for the piece.
        If the Piece can't move anywhere, it will return False. Otherwise,
        return True.

        @return:
        boolean: True if there was a valid movement to be made by the piece,
                 False if the piece couldn't move anywhere
        """
        tries = 0
        random_movement_made = self.random()
        while not random_movement_made:
            random_movement_made = self.random()
            tries += 1
            if tries >= len(self.possible_movements):
                return False
        return True

class Attacking(Action):
    def __init__(self, piece, attack_functions):
        Action.__init__(self, piece, attack_functions)
        self.possible_attacks = self.possible_actions

    def __default_actions(self, piece):
        return self._normal_default_actions()

