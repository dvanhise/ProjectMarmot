from game_objects.tag import TagManager


class Vector:

    def __init__(self, name='Default', default_ward=0, tags=None):
        self.name = name
        self.tags = TagManager(tags)
        self.default_ward = default_ward
