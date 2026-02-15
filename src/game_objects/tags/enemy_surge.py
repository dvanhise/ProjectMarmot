from src.game_objects.tag import Tag


class EnemySurge(Tag):
    id = 'surge'
    name = 'Surge'
    icon = 'power'
    tooltip = 'Increases all payload power by {count}.'

    def on_script_creation(self, script):
        script.power += self.count
