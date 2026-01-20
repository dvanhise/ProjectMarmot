class Vector:

    def __init__(self, name='Default', power_boost=0, default_ward=0):
        self.name = name
        self.power_boost = power_boost
        self.default_ward = default_ward

        # on_trigger: Callable = None
        # on_install: Callable = None
        # on_attack: Callable = None
