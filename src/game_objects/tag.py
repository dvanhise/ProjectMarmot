class Tag:
    id = ''
    icon = ''
    tooltip = ''
    count = 0
    card = ''

    part_of_vector = False
    remove_on_vector_change = False

    def __init__(self, count):
        self.count = count

    def get_tooltip(self):
        return self.tooltip.format(count=self.count, card=self.card)

    def get_full_name(self):
        return self.id

    def before_node_encounter(self):
        pass

    def after_failed_script_node_encounter(self, script, node):
        pass

    def after_successful_script_node_encounter(self, script, node):
        pass

    def on_friendly_script_node_encounter(self, script, node):
        pass

    def on_turn_end_node(self, node):
        pass

    def on_turn_end_player(self, player):
        pass

    def on_turn_end_vector(self, vector, node):
        pass

    def on_vector_install(self):
        pass

    def on_script_execution(self, script):
        pass