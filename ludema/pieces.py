import random
from functools import wraps
from ludema.abstract.piece import Piece
from ludema.abstract.actions import Action
from ludema.abstract.utils import Direction
from ludema.exceptions import (PieceDoesNotHaveItemError, PieceIsNotOnATileError,
                               PieceIsNotOnThisBoardError, OutOfBoardError,
                               PositionOccupiedError, NoItemToGrab)

class Wall(Piece):
    """A very simple piece to represent walls."""
    def __init__(self, letter="."):
        Piece.__init__(self, letter)

class Item(Piece):
    """A class to represent items which can be owned and used by players
    and NPCs alike. It's intended to be subclassed as to define their action.
    """
    def __init__(self, letter, name, owner=None):
        """Initiates an item.

        @args:
        letter (str): the letter by which the item will be represented
        name (str): the name of the item
        owner (Piece, ~None): the owner of the piece.
        """
        Piece.__init__(self, letter, name)
        self.owner = owner

    @property
    def has_owner(self):
        """Return True if the Item has an owner, False otherwise."""
        return False if self.owner is None else True

    def do_action(self):
        raise NotImplementedError("Every item should have its own do_action method!")

class ShortRangeItem(Item):
    """A class to represent items which can only affect its surroundings,
    both if carried by an owner of if it lies on the ground.
    """
    def __init__(self, letter, name, owner=None):
        """Initiates a short range item.

        @args:
        letter (str): the letter by which the item will be represented
        name (str): the name of the item
        owner (Piece, ~None): the owner of the piece.
        """
        Item.__init__(self, letter, name, owner)

    @property
    def range(self):
        """A list containing all the Tiles which would be affected by this
        item if used.

        May be None if the Item has no owner and it hasn't been put onto a
        map yet.
        """
        def only_valid_from(s): return list(filter(lambda t: t is not None, s))

        if self.owner:
            return only_valid_from(self.owner.surroundings.values())
        else:
            return only_valid_from(self.surroundings.values()) if self.home_tile else None

    def do_action(self):
        raise NotImplementedError("Every item should have its own do_action method!")


class Character(Piece):
    """A baseclass for all characters, be them the Player, NPCs or enemies.
    Should not be used directly.
    """
    def __init__(self, letter, name, movements=None, attack_damage=1,
                 items=None, health=10):
        """Init a Character.

        @args:
        letter (str): the letter by which the item will be represented
        name (str): the name of the item
        movements ([nullary functions] | [] | ~None): leave None
            so the Character will have the defaults movements (up, down, left, right).
            Pass a list of nullary functions to specify your own movement functions.
            Pass an empty list to explictly set no movements for this Character.
        attack_damage (int, ~1): how much damage should this piece do when attacking
        items ([Items] | ~None): the Items this piece should start with.
            if None, items will be an empty list.
        health (int, ~10): how much health should this character have.
        """
        Piece.__init__(self, letter, name, movements)
        self.items = items or []
        self.health = health
        self.attack_damage = attack_damage

    @property
    def is_dead(self):
        """Return True if health is below 0, False otherwise."""
        return False if self.health > 0 else True

    def _unsafe_use_item(self, item):
        """Uses item _item_ on the home_map of the character. Returns
        the action specified by the item.

        @args:
        item (Item): the item to be used

        @raise:
        PieceDoesNotHaveItemError, PieceIsNotOnATileError

        @return:
        action, the return value of calling item.do_action()
        """
        if item not in self.items:
            raise PieceDoesNotHaveItemError(self, item)
        if not self.surroundings:
            raise PieceIsNotOnATileError

        self.items.remove(item)
        action = item.do_action()
        return action

    def use_item(self, item):
        """Safely uses an item.

        @args:
        item (Item): the item to be used

        @return
        (True, action) if the item could be used. action is the return value
            of calling item.do_action()
        (False, None) if the item could not be used.
        """
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

    def do_passive_action(self):
        pass

    def do_active_action(self):
        pass


class Player(Character):
    """The Player character. The most important characteristic of the Player
    is that some of its methods, when called, will make the board in which
    this Player live advance one turn."""
    def __init__(self, letter, name, movements=None,
                 attack_damage=1, items=None, health=10):
        Character.__init__(self, letter, name, movements, attack_damage,
                           items, health)
        self.turn_passing_actions = ['use_item', 'grab_item', 'move']

    def __pass_turn(self, func):
        @wraps(func)
        def pass_wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            home_tile = object.__getattribute__(self, 'home_tile')
            if home_tile is not None:
                home_tile.board.turn += 1
            else:
                raise PieceIsNotOnATileError(self)
            return res
        return pass_wrapper

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if name in object.__getattribute__(self, 'turn_passing_actions'):
            if isinstance(attr, Action):
                attr.do = self.__pass_turn(attr.do)
            else:
                attr = self.__pass_turn(attr)
        return attr


class NPC(Character):
    def __init__(self, letter, name, movements=None, attack_damage=1,
                 items=None, health=10):
        Character.__init__(self, letter, name, movements, attack_damage,
                           items, health)

