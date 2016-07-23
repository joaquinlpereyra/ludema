class Map():
    """Defines a simple square map where character can move.
    A map is a list of lists where
    """
    def __init__(self, size_x, size_y):
        """Initializates a simple matrix to represent the map"""
        row = [0 for _ in range(size_x)]
        self.board = list(reversed(([row.copy() for _ in range(size_y)])))

    def __repr__(self):

    def put_object(self, world_object):
        """Puts an object in the board. Return None."""
       position_x, position_y = world_object.pos_x, world_object.pos_y
       place = self.board[position_y][position_x]
       if isinstance(place, _WorldObject):
           print("WARNING: There's something already there!")
       else:
           self.board[position_y][position_x] = world_object



class _WorldObject():
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

class Door(_WorldObject):
    def __init__(self, pos_x, pos_y, is_open=False):
        _WorldObject.__init__(self, pos_x, pos_y)
        self.is_open = is_open
