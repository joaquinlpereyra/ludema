class _Item:
    def __init__(self, owner=None):
        self.is_owned = is_owned
        self.owner = owner

    def has_owner(self):
        return False if owner is None else True

    def do_action(self):
        raise NotImplementedError("Every item should have its own do_action method!")

class Key(_Item):
    def __init__(self, target_door, owner=None):
        _Item.__init__(owner)
        self.taget_door = target_door

    def do_action(self):
        ### TODO: NEEDS IMPLEMENTING
        return self.open_door()

