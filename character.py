class Character():

    def __init__(self, name, pos, items=None):
        """Name as a string, objects as list of Item objects"""
        self.name = name
        self.items = items or []
        self.pos = pos

    def where_is_she(self):
        return self.pos
