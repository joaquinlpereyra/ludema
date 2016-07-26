class _Item:
    def __init__(self, owner=None):
        self.owner = owner

    @property
    def has_owner(self):
        return False if owner is None else True

    def do_action(self):
        raise NotImplementedError("Every item should have its own do_action method!")

class Key(_Item):
    def __init__(self, target_door, owner=None):
        _Item.__init__(owner)
        self.letter = " K "
        self.taget_door = target_door

    def do_action(self):
        return self.open_door()

    def open_door(self):
        owner = self.owner
        doors = filter(lambda item: isinstance(item, Door), owner.surroundings)
        if doors:
            for door in doors:
                if door is target_door:
                    target_door.is_open = True
                    break
            else:
                print("Look's like this key is not made for any of these doors!")
        else:
            print("Dude, there are not even doors around")
        return self.target_door, doors
