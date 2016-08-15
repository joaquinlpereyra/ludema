from ludema.exceptions import (PieceDoesNotHaveItemError, PieceIsNotOnATileError,
                             PieceIsNotOnThisBoardError, OutOfBoardError,
                             PositionOccupiedError, NoItemToGrab)
from ludema.utils import Direction
import random


class Piece:
    """Defines a Piece, which is _anything_ that can
    be represented on the map.

    Not intended to be used directly but rather should be used
    as superclass.
    """

    def __init__(self, letter, name=None, walkable=False):
        """Initializes a Piece with a given name, letter and its home tile
        on None. The home tile should only be set by assigning the piece
        to a tile.

        args:
        letter (string) [len(string) == 1]: representation of piece on board
        name (string | None): Defaults to None. Name of the piece. Leave None
            for anonymous.
        walkable (bool): Defaults to False. Can the piece be walked over by
            other pieces?
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
        pass

class MovablePiece(Piece):

    class Movements:
        """This clase represents the 'Move' interface owned by a MovablePiece
        instance.
        It's job is to hold functions that move the MovablePiece in a direction.
        It also holds a list with all the posible movements the Piece can do,
        so you can choose one at random or inspect them dynamically.
        """
        def __init__(self, piece, movement_functions=None):
            """Starts the object with an empty list of possible movements and
            forces it to have at least the deafult ones.

            @args:
            piece (MovablePiece): the movable piece to which the movements refer
            movement_functions ([nullary functions]): a list of valid
                functions which as a side effect move the piece.
            """
            self.possible_movements = []
            if movement_functions is None or movement_functions == []:
                self.__default_movements(piece)
            else:
                self.__set_movements(movement_functions)

        def __default_movements(self, piece):
            """Create and set the default movement functions (up, down, left,
            right)

            @args:
            piece (MovablePiece): the MovablePiece to be moved

            @return:
            None
            """
            def up(): return piece.move_to_tile(piece.surroundings[Direction.UP])
            def right(): return piece.move_to_tile(piece.surroundings[Direction.RIGHT])
            def down(): return piece.move_to_tile(piece.surroundings[Direction.DOWN])
            def left(): return piece.move_to_tile(piece.surroundings[Direction.LEFT])
            self.__set_movements([up, right, down, left])

        def __set_movements(self, movement_functions):
            """Append every movement_function to the list of possible movements
            and sets them as method of the instance.

            @args:
            movement_functions ([nullary functions]): a list of valid
                functions which as a side effect move the piece.

            @return:
            None
            """
            for movement_function in movement_functions:
                self.possible_movements.append(movement_function)
                setattr(self, movement_function.__name__, movement_function)

        def random(self):
            """Call and return a random function from the possible movements
            list. Keep in mind that the movement may or may not be effective,
            depending on the current position of the piece and where
            the movement tries to send the piece. For a random valid movent,
            call the random_and_valid method.
            """
            surprise_move = random.choice(self.possible_movements)
            was_movement_valid = surprise_move()
            return was_movement_valid

        def random_and_valid(self):
            """Call and return a random function from the possible movements,
            making sure that the movement is actually possible for the piece.
            If the Piece can't move anywhere, it will return False. Otherwise,
            return True.
            """
            tries = 0
            random_movement_made = self.random()
            while not random_movement_made:
                random_movement_made = self.random()
                tries += 1
                if tries >= len(self.possible_movements):
                    return False
            return True



    def __init__(self, letter, name, movements=None, walkable=False):
        """Create a MovablePiece. A MovablePiece is a Piece which exposes
        the 'Movement' interface, dictated by the movements paramether.

        The interface notation is: my_piece.move.my_movement_functions_name()
        For example: John.move.up() will move John up a tile.

        move.up(), move.down(), move.right() and move.left() are the movements
        by default provided if you don't specify any movement functions of your
        own.

        Movement functions are nullary functions which move the piece as
        a side effect. You probably also want them to return the value of
        that operation. They look something like this (brances indicate
        non mandatory but recommended return):
        def move(): [return] piece.move_to_tile(destiny_tile).

        An example of a valid movement function, the default up movement:
        def up(): return piece.move_to_tile(piece.surroundings[Direction.UP])

        args:
        letter (string): letter representation of the piece on the board
        name (string): name of the piece
        movements ([nullary functions] | None): Defaults to None. The list
            of movement functions for the piece. If None, default movements
            (up, down, right, left a tile) will be given.
        walkable (bool): Defaults to False. Dictates if other pieces
            can move above this piece.
        """

        Piece.__init__(self, letter, name, walkable)
        self.move = MovablePiece.Movements(self, movements)

    def _unsafe_move_to_tile(self, tile):
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

    def move_to_tile(self, tile):
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
                return self._unsafe_move_to_tile(tile)
            except (PieceIsNotOnATileError, PieceIsNotOnThisBoardError):
                return False
        else:
            return False

class Item(Piece):
    def __init__(self, name, letter, owner=None):
        Piece.__init__(self, name, letter)
        self.owner = owner

    @property
    def has_owner(self):
        return False if self.owner is None else True

    def do_action(self):
        raise NotImplementedError("Every item should have its own do_action method!")

class ShortRangeItem(Item):
    def __init__(self, name, letter, owner=None):
        Item.__init__(self, name, letter, owner)

    @property
    def range(self):
        def only_valid_from(s): return list(filter(lambda t: t is not None, s))

        if self.owner:
            return only_valid_from(self.owner.surroundings.values())
        else:
            return only_valid_from(self.surroundings.values()) if self.home_tile else None

    def do_action(self):
        raise NotImplementedError("Every item should have its own do_action method!")


class Wall(Piece):
    def __init__(self, letter="."):
        Piece.__init__(self, letter)


class Character(MovablePiece):
    """A baseclass for all characters, be them the Player, NPCs or enemies.
    Should not be used directly.
    """
    def __init__(self, letter, name, movements=None, attack_damage=None,
                 items=None, health=10):
        MovablePiece.__init__(self, letter, name, movements)
        self.letter = letter
        self.name = name
        self.items = items or []
        self.health = health
        self.attack_damage = attack_damage

    @property
    def is_dead(self):
        return False if self.health else True

    def _unsafe_attack(self, attack_tile):
        if not self.attack_damage:
            raise CharacterCantAttackError(self)
        if not isinstance(attack_tile.piece, Character):
            raise TileDoesntHaveACharacterError(self, attack_tile)

        attacked_character = attack_tile.piece
        attacked_character.health -= self.attack_damage

    def attack(self, attack_tile):
        try:
            self._unsafe_attack(attack_tile)
            return True
        except (CharacterCantAttackError, TileDoesntHaveACharacterError):
            return False

    def _unsafe_use_item(self, item):
        """Uses item _item_ on the home_map of the character. Returns
        the action specified by the item."""
        if item not in self.items:
            raise PieceDoesNotHaveItemError(self, item)
        if not self.surroundings:
            raise PieceIsNotOnATileError

        self.items.remove(item)
        action = item.do_action()
        return action

    def use_item(self, item):
        try:
            action = self._unsafe_use_item(item)
            return True, action
        except (PieceDoesNotHaveItemError, PieceIsNotOnATileError):
            return False, None

    def _unsafe_grab_item(self, tile_where_item_is):
        if not isinstance(tile_where_item_is.piece, Item):
            raise NoItemToGrab(self)

        self.items.append(tile_where_item_is.piece)
        tile_where_item_is.piece.owner = self
        tile_where_item_is.piece = None

    def grab_item(self, tile_where_item_is):
        try:
            self._unsafe_grab_item(tile_where_item_is)
            return True
        except NoItemToGrab:
            return False

    def grab_item_from_surroundings(self):
        for tile in filter(lambda i: i is not None, self.surroundings.values()):
            item_grabbed = self.grab_item(tile)
            if item_grabbed:
                return True
        else:
            return False


class Player(Character):
    """The Player character. The most important characteristic of the Player
    is that some of its methods, when called, will make the board in which
    this """
    def __init__(self, letter, name, movements=None,
                 attack_damage=1, items=None, health=10):
        Character.__init__(self, letter, name, movements, attack_damage,
                           items, health)
        self.turn_passing_actions = ['use_item', 'grab_item', 'move_to_tile']

    def __getattribute__(self, name):
        if name in object.__getattribute__(self, 'turn_passing_actions'):
            home_tile = object.__getattribute__(self, 'home_tile')
            if home_tile is not None:
                home_tile.board.turn += 1
            else:
                raise PieceIsNotOnATileError(self)
        return object.__getattribute__(self, name)


class NPC(Character):
    def __init__(self, letter, name, movements=None, attack_damage=None,
                 items=None, health=10):
        Character.__init__(self, letter, name, movements, attack_damage,
                           items, health)

    def do_passive_action(self):
        pass

    def do_active_action(self):
        pass
