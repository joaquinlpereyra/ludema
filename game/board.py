class Map:
    """Defines a simple square map where character can move.
    The map main attribute is the board, which is represented as a
    matrix, for example like this for a 3x3 board:
    board = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]

    On maps, all integers represent "NOTHINGNESS". All other objects
    shown on maps should be a subclass of _WorldObject.

    0: represents complete nothingness
    1: represents place where a _WorldObject _was_ but is not anymore
    2: represents place where an Item _was_ but is not anymore

    When trying to extract or set information to the board, you should
    do it like this board[y_coordinate][x_coordinate]
    """
    def __init__(self, size_x, size_y):
        """Initializates a simple matrix to represent the map.
        """
        row = [0 for _ in range(size_x)]
        self.board = [row.copy() for _ in range(size_y)]

    def __str__(self):
        """How the string will be printed.
        A . (dot) for integers, represeting emptiness.
        For everything else, print the letter attribute of the object.
        """
        map_ = ""
        for row in self.board:
            map_ += "."
            for index, object_ in enumerate(row):
                if isinstance(object_, int):
                    map_ += "   "
                elif isinstance(object_, _WorldObject):
                    map_ += object_.letter
                elif isinstance(object_, Item):
                    if not object_.has_owner:
                        map_ += object_.letter
            map_ += ". \n"
        return map_

    def __repr__(self):
        """Return the graphical representation of the map
        plus the classical python representation of an object.
        """
        return self.__str__() + '\n' + super().__repr__()

    def put_object(self, world_object):
        """Puts an object in the board. Returns True if object
        could be put correctly, False if not.
        """
        position_x = world_object.position_x
        position_y = world_object.position_y

        if not self.is_valid_position(position_x, position_y):
            print("Looks like something is already there... or maybe "
                  "I'm going too far away?")
            now_on_map = False

        else:
            place = self.board[position_y][position_x]
            self.board[position_y][position_x] = world_object
            world_object.home_map = self
            now_on_map = True
        return now_on_map

    def move_object(self, old_x, old_y, new_x, new_y):
        """Moves object found on old_position to new_position.
        old_position and new_position must tuples of (x,y) coordinates
        Return True if it was moved, False if not.
        """
        if self.is_valid_position(new_x, new_y):
            self.board[new_y][new_x] = self.board[old_y][old_x]
            self.board[old_y][old_x] = 0
            was_moved = True
        else:
            print("Well, I really can't move there...")
            was_moved = False
        return was_moved


    def remove_object(self, object_position_x, object_position_y):
        """Removes an object from the map given its position.
        Of course, we cannot remove nothingness from the map.
        Returns the deleted object if an object was found, None
        if nothingness was found.
        """
        object_ = self.board[object_position_y][object_position_x]
        if isinstance(object_, _WorldObject):
            self.board[object_position_y][object_position_x] = 1
            return object_
        elif isinstance(object_, Item):
            self.board[object_position_y][object_position_x] = 2
        else:
            return None

    def is_valid_position(self, pos_x, pos_y):
        """Returns False if the position is not valid (ie: not inside map
        or already occupied). True otherwise.
        """
        conditions = (self._is_position_outside_map,
                      self._is_position_occupied,
                      self._is_position_negative)

        for condition in conditions:
            condition_failed = condition(pos_x, pos_y)
            if condition_failed:
                valid_position = False
                break

        # an else clause after a loop means 'execute if the loop actually
        # looped trought everything'
        else:
            valid_position = True

        return valid_position

    def _is_position_outside_map(self, pos_x, pos_y):
        """Return True if a given position is found within the limits
        of the board.  """
        if len(self.board) > pos_y and len(self.board[pos_y]) > pos_x:
            is_outside = False
        else:
            is_outside = True
        return is_outside

    def _is_position_negative(self, pos_x, pos_y):
        if pos_x < 0 or pos_y < 0:
            return True
        else:
            return False

    def _is_position_occupied(self, pos_x, pos_y):
        """Return True if a given position if already occupied by other
        object.
        """
        if isinstance(self.board[pos_y][pos_x], int):
            is_occupied = False
        else:
            is_occupied = True
        return is_occupied

class _WorldObject:
    """Defines a WorldObject, which is _anything_ that can
    be represented on the map.

    Not intended to be used directly but rather should be used
    as superclass.
    """
    def __init__(self, position_x, position_y):
        """Initializates an object with a given position
        and its associated map startin on None.
        """
        self.home_map = None
        self.position_x = position_x
        self.position_y = position_y

    def get_surroundings(self):
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
        if self.home_map is None:
            return None

        map_ = self.home_map.board
        surroundings = []

        up = (self.position_x, self.position_y - 1)
        left = (self.position_x - 1, self.position_y)
        down = (self.position_x, self.position_y + 1)
        right = (self.position_x + 1, self.position_y)

        for position in (up, right, down, left):
            if self.home_map.is_valid_position(position[0], position[1]):
                surroundings.append(map_[position[0]][position[1]])
            else:
                surroundings.append(None)

        return surroundings

    def move(self, direction):
        """Move the object in a certain direction.
        If the object has an associated map, move the object there too.
        """
        dispatch = {"right" : self.__move_right,
                    "left" : self.__move_left,
                    "up" : self.__move_up,
                    "down" : self.__move_down}

        old_pos = (self.position_x, self.position_y)
        dispatch[direction]()
        new_pos = (self.position_x, self.position_y)

        if self.home_map:
            moved_success = self.home_map.move_object(old_pos[0], old_pos[1],
                                                      new_pos[0], new_pos[1])
            if not moved_success:
                # if it couldn't be moved, restore my position to original
                # values
                self.position_x = old_pos[0]
                self.position_y = old_pos[1]

        return self.position_x, self.position_y

    def __move_up(self):
        self.position_y -= 1

    def __move_down(self):
        self.position_y += 1

    def __move_right(self):
        self.position_x += 1

    def __move_left(self):
        self.position_x -= 1


class Character(_WorldObject):
    """The user Character. This will be controlled by the
    user."""
    def __init__(self, pos_x, pos_y, name, items=[]):
        _WorldObject.__init__(self, pos_x, pos_y)
        self.letter = " \u03A8 " # 'Ψ'
        self.name = name
        self.items = items

    def use_item(self, item):
        """Uses item _item_ on the home_map of the character. Returns
        the action specified by the item."""

        def item_is_usable(item):
            """Check if item is usable by the character."""
            if not isinstance(item, Item):
                print("That's not really an item, dude...")
                usable = False
            elif item not in self.items:
                print("Mhmm... you don't really have that. How could you use it?")
                usable = False
            else:
                usable = True
            return usable

        if item_is_usable(item):
            #XXX: ITEM CLASS STILL NEEDS IMPLEMENTING
            self.items.remove(item)
            action = item.do_action(self.home_map)
        else:
            action = None

        return action

class NPC(_WorldObject):
    """A non-playable character."""
    # TODO: implement
    # XXX: Should this inherit from Character, too? After all, it is a
    # non playable CHARACTER.
    pass

class Door(_WorldObject):
    """A simple door."""
    def __init__(self, pos_x, pos_y, is_open=False):
        _WorldObject.__init__(self, pos_x, pos_y)
        self.letter = " D* " if is_open else " D "
        self.is_open = is_open

