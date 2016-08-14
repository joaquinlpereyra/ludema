from ludema.pieces import Piece

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
            return only_valid_from(self.owner.surroundings)
        else:
            return only_valid_from(self.surroundings) if self.home_tile else None

    def do_action(self):
        raise NotImplementedError("Every item should have its own do_action method!")

