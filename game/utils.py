from collections import namedtuple

# this namedtuple thing is very interesting: http://goo.gl/Xs5fx5
Position = namedtuple('Position', ('x', 'y'))

class Direction:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
