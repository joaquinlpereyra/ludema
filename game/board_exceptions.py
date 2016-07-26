class _BoardError(Exception):
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

class OutOfBoardError(_BoardError):
    def __init__(self, pos_x, pos_y):
        BoardError.__init__(self, pos_x, pos_y)

    def __str__(self):
        return ("The position {0}, {1} doesn' exist"
               "on this map".format(self.pos_x, self.pos_y))

class PositionOccupiedError(_BoardError):
    def __init__(self, pos_x, pos_y):
        BoardError.__init__(self, pos_x, pos_y)

    def __str__(self):
        return ("The position {0}, {1} is already "
               "occuppied".format(self.pos_x, self.pos_y))
