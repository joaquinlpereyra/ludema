import random
from functools import wraps
from ludema.abstract.utils import Direction
from ludema.exceptions import (PieceIsNotOnATileError,
                               PieceIsNotOnThisBoardError,
                               TileIsEmptyError)

class Action:
    def __init__(self, piece, action_functions):
        self.possible_actions = []
        self.piece = piece
        if action_functions is None:
            action_functions = self._default_actions()
        self._set_actions(action_functions)
        self.history = []

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if attr in object.__getattribute__(self, 'possible_actions'):
            attr = self._history_appender(attr)
        return attr

    @property
    def is_implemented(self):
        return True if self.possible_actions else False

    def _history_appender(self, func):
        @wraps(func)
        def history_wrapper(*args, **kwargs):
            self.history.append(func.__name__)
            return func(*args, **kwargs)
        return history_wrapper

    def _increment_piece_home_board_turn(self):
        self.piece.home_tile.board.turn += 1

    def _normal_default_actions(self):
        """Just a collection of four extremely normal set of default actions.
        The ones who apply the action to the tile up, right, left and down
        of the piece.
        """
        def up():
            return self.do(self.piece.surroundings[Direction.UP])
        def right():
            return self.do(self.piece.surroundings[Direction.RIGHT])
        def down():
            return self.do(self.piece.surroundings[Direction.DOWN])
        def left():
            return self.do(self.piece.surroundings[Direction.LEFT])
        return [up, right, down, left]

    def _set_actions(self, action_functions):
        """Sets the action_funcions as methods of the class
        and append them to the possible_actions list.
        """
        for action_function in action_functions:
            self.possible_actions.append(action_function)
            setattr(self, action_function.__name__, action_function)

    def _default_actions(self):
        """These will be the default action functions. Every action should
        implement them, but the _normal_default_actions method give you
        four extremely common default function actions: the one which
        applies the action to the tiles above, at right, below and at left
        of the piece.

        Every action class should implement this.
        """
        raise NotImplementedError("The Action class shouldn't be used directly!")

    def _unsafe_do(self, tile):
        """Intended to actually perform the action. Should check all
        action conditions and raise an appropiate error if they are not met.
        Doesn't need to return anything. Shouldn't be used for I/O, instead
        use the do method for that.

        Every action should implement this method.
        """
        raise NotImplementedError("The Action class shouldn't be used directly!")

    def do(self, tile, dont_pass_turn=False):
        """Inteded as a safe wraper for _unsafe_do. Should take a tile
        indicating where the action must be performed. Should return a bolean
        indicating if the action could be performed or not. Should be capable
        of handling I/O without raising any exceptions.

        Useful for one-use-cases for the actions, if you want to extraordinarily
        perform an action to a tile. For ordinary uses, use the actions in the
        possible_actions lists. For example, if a piece moves up,down,left,right
        alsways, set those as actions functions. If a magician teleports the
        piece somewhere, you can use this function to move it there.

        All the action functions should ultimately use this method.

        Every action should implement this method.
        """
        raise NotImplementedError("The Action class shouldn't be used directly!")

    def random(self):
        """Call a random function from the possible actions
        list. Keep in mind that the action may or may not be performed,
        depending on the current position of the piece and what the action
        tries to do.

        @return:
        boolean, True if action was performed, False if not
        """
        surprise_action = random.choice(self.possible_actions)
        was_action_valid = surprise_action()
        return was_action_valid

    def random_and_valid(self):
        """Call a random function from the possible actions,
        making sure that the action is actually possible for the piece.
        If no actions from the list of possible actions, it will just return
        False.

        @return:
        boolean: True if there was a valid action to be made by the piece,
                 False if the piece couldn't move anywhere
        """
        tries = 0
        random_action_performed = self.random()
        while not random_action_performed:
            random_action_performed = self.random()
            tries += 1
            if tries >= len(self.possible_actions):
                return False
        return True

    def all(self):
        """Call all possible actions from the list. The actions may or may
        not be performed depending on the action conditions.

        @return:
        A dicionary of {action_function_name, boolean} key-value pairs,
        indicating which actions where actually performed (True) and which
        not (False).
        """
        successes = {}
        for action_function in self.possible_actions:
            success = action_function()
            successes[action_function.__name__] = success
        return successes

    def until_success(self):
        """Call all possible actions from the list of possible actions,
        but stop once it can perform one successfully.

        @return:
        boolean: True if there was a valid action performed by the piece,
                 False if no valid action was found.
        """
        for action_function in self.possible_actions:
            success = action_function()
            if success:
                return True
        else:
            return False

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

        @return:
        None
        """
        return self._normal_default_actions()

    def _unsafe_do(self, tile):
        """Move the object if it can.
        That means: unlink the piece from its current tile and link it
        to the new tile; unless there's a piece in the destiny tile already.

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
            # what if tile.piece.on_touch_do actually moved the touched piece?
            # it could have, so we need to check if tile.piece still has
            # a piece...
            if tile.piece and not tile.piece.walkable:
                return False

        self.piece.home_tile.piece = None
        tile.piece = self.piece
        return True

    def do(self, tile):
        """Move the object, if it can.

        @args:
        tile (Tile): the tile to which the piece will try to move.

        @return:
        bool: True if piece could be moved, False if not
        """

        if tile:
            try:
                return self._unsafe_do(tile)
            except (PieceIsNotOnATileError, PieceIsNotOnThisBoardError):
                return False
        else:
            return False

class Attacking(Action):
    def __init__(self, piece, attack_functions):
        Action.__init__(self, piece, attack_functions)
        self.possible_attacks = self.possible_actions

    def _default_actions(self):
        """Create and set the default attack functions (up, down, left,
        right)

        @return:
        None
        """
        return self._normal_default_actions()

    def _unsafe_do(self, tile):
        """Attack a piece on tile passed as argument. If tile
        has no piece, raise a TileIsEmptyError.

        @args:
        tile (Tile): the tile which the piece will try to attack

        @return:
        None
        """
        if tile.piece is None:
            raise TileIsEmptyError(self.piece, tile)

        attacked_piece = tile.piece
        attacked_piece.health -= self.piece.attack_damage

    def do(self, tile):
        """Attack a tile passed as argument. Safe to use for I/O, should
        never raise an error.

        @args:
        tile (Tile): the tile which the piece will try to attack

        @return:
        bool: True if attack could be performed, False if attack failed
        (because the tile didn't have a piece associated or it was None)
        """
        if tile:
            try:
                self._unsafe_do(tile)
                return True
            except TileIsEmptyError:
                return False
        else:
            return False
