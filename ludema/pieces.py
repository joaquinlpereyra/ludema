import random
from functools import wraps
from ludema.abstract.piece import Piece
from ludema.abstract.actions import Action
from ludema.abstract.utils import Direction
from ludema.exceptions import (PieceDoesNotHaveItemError, PieceIsNotOnATileError,
                               PieceIsNotOnThisBoardError, OutOfBoardError,
                               PositionOccupiedError, NoItemToGrab)

class Wall(Piece):
    def __init__(self, letter="."):
        """A very simple piece to represent walls.

        Args:
            letter (str): the letter which shall be used to represent it on the board
        """
        Piece.__init__(self, letter)

class Item(Piece):
    def __init__(self, letter, name, owner=None):
        """A class to represent items which can be owned and used by players
        and NPCs alike. It's intended to be subclassed as to define their action.

        Args:
            letter (str): the letter by which the item will be represented
            name (str): the name of the item
            owner (Piece): the owner of the item.

        Warning:
            This class should not be used directly, but rather as a subclass
            for your own items.
        """
        Piece.__init__(self, letter, name)
        self.owner = owner

    @property
    def has_owner(self):
        """True if the Item has an owner, False otherwise."""
        return False if self.owner is None else True

    def do_action(self):
        """This method will be called when a Character uses the item.

        Warning:
            All subclasses should implement this method.
        """
        raise NotImplementedError("Every item should have its own do_action method!")

class ShortRangeItem(Item):
    def __init__(self, letter, name, owner=None):
        """A class to represent items which can only affect its surroundings,
        both if carried by an owner of if it lies on the ground.

        Args:
            letter (str): the letter by which the item will be represented
            name (str): the name of the item
            owner (Piece): the owner of the item.

        Warning:
            This class should not be used directly, but rather as a subclass
            for your own items.
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


class Character(Piece):
    def __init__(self, letter, name, movements=None, attack_damage=1,
                 items=None, health=10):
        """A baseclass for all characters, be them the Player, NPCs or enemies.

        Args:
            letter (str): the letter by which the item will be represented
            name (str): the name of the item
            movements ([nullary functions] | [] | None): leave None
                so the Character will have the defaults movements (up, down, left, right).
                Pass a list of nullary functions to specify your own movement functions.
                Pass an empty list to explictly set no movements for this Character.
            attack_damage (int): how much damage should this piece do when attacking
            items ([Items]): the Items this piece should start with.
                If left None, items will be an empty list.
            health (int): how much health should this character have.

        Warning:
            This class should not be used directly, but rather subclassed to create
            your own Characters.

            If you're looking for a class for the main character, use or subclass
            :class:`~ludema.pieces.Player`. If you want an NPC,
            either friendly or unfriendly, use :class:`~ludema.pieces.NPC`.
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

    def do_passive_action(self):
        """This method will be called whenever a turn passes on the board
        this Character lives in. Default behavior is to do nothing. Feel free
        to override.

        Note:
            You must respect the method's signature, that is, this method
            should take no parameters appart from self.
        """
        pass

    # TODO: implement
    def __do_active_action(self):
        pass


class Player(Character):
    def __init__(self, letter, name, movements=None, attack_damage=1, items=None,
                 health=10, turn_passing_actions=None):
        """The Player character. The most important characteristic of the Player
        is that some of its methods, when called, will make the board in which
        the Player lives advance one turn.

        Args:
            movements ([nullary functions] | [] | None): leave None
                so the Character will have the defaults movements (up, down, left, right).
                Pass a list of nullary functions to specify your own movement functions.
                Pass an empty list to explictly set no movements for this Character.
            attack_damage (int): how much damage should this piece do when attacking
            items ([Items]): the Items this piece should start with. Leave None to
                start with no items.
            health (int): how much health should this character have.
            turn_passing_actions ([str]): all the elements of the list should be
                either method names or actions names. when in this list,
                using one of these methods or using the Action.do method will
                pass a turn on the character's board. If left on None,
                moving, grabbing an item and attacking will pass a turn.
        """
        Character.__init__(self, letter, name, movements, attack_damage,
                           items, health)
        self.turn_passing_actions = turn_passing_actions or ['use_item', 'grab_item', 'move']

    def __pass_turn(self, func):
        """A decorator which makes a function pass a turn on the character's
        home board.
        """
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
        """Overriden __getattribute__ so that it applies the __pass_turn
        decorator to the methods or actions on self.turn_passing_actions.
        """
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
