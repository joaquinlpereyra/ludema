class Map():
    """Defines a simple square map where character can move.
    A map is a list of lists where
    """
    def __init__(self, size_x, size_y):
        row = [0 for _ in range(size_x)]
        self.board = [row for _ in range(size_y)]

    def put_door_at(x, y):

