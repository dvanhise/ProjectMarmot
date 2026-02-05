class Tag:
    id = ''
    name = 'TODO'
    icon = ''
    tooltip = 'TODO'
    count = 0
    card = ''
    positive = True

    part_of_vector = False
    remove_on_vector_change = False

    def __init__(self, count):
        self.count = count

    def get_tooltip(self):
        return f'{self.name}: {self.tooltip.format(count=self.count, card=self.card)}'

    def get_generic_tooltip(self):
        return f'{self.name}: {self.tooltip.format(count='N', card='Card')}'

    def get_full_name(self):
        return self.name

    def on_change(self, change):
        # Any time a tag is modified
        pass

    def before_script_node_encounter(self, script, node):
        pass

    def after_failed_script_node_encounter(self, script, node):
        pass

    def after_successful_script_node_encounter(self, script, node):
        pass

    def on_friendly_script_node_encounter(self, script, node):
        pass

    def on_node_captured(self, node):
        # When an opponent captures a node
        pass

    def on_vector_install(self, node, vector, player_info):
        pass

    def on_turn_end_node(self, node):
        pass

    def on_turn_end_player(self, player):
        pass

    def on_turn_end_enemy(self, enemy):
        pass

    def on_turn_end_vector(self, vector, node):
        pass

    def on_turn_start_player(self, player):
        pass

    def on_script_execution(self, script):
        pass

    def on_temp_card_creation(self, card, player_info):
        # When temp cards are created before a level starts and during play
        pass


class TagManager(list):

    def __init__(self, initial_tags=None):
        super().__init__()
        [self.add_tag(tag) for tag in initial_tags or []]

    def add_tag(self, tag: Tag):
        combined = False
        for t in self:
            if t.id == tag.id:
                t.count += tag.count
                t.on_change(tag.count)
                combined = True
        if not combined:
            self.append(tag)
            tag.on_change(tag.count)

    def find_tag(self, cls):
        for tag in self:
            if tag.__class__ == cls:
                return tag
        return None

    def remove_depleted_tags(self):
        for tag in self:
            if tag.count <= 0:
                self.remove(tag)

    def before_script_node_encounter(self, script, node):
        for tag in self:
            tag.before_script_node_encounter(script, node)
        self.remove_depleted_tags()

    def after_failed_script_node_encounter(self, script, node):
        for tag in self:
            tag.after_failed_script_node_encounter(script, node)
        self.remove_depleted_tags()

    def after_successful_script_node_encounter(self, script, node):
        for tag in self:
            tag.after_successful_script_node_encounter(script, node)
        self.remove_depleted_tags()

    def on_friendly_script_node_encounter(self, script, node):
        for tag in self:
            tag.on_friendly_script_node_encounter(script, node)
        self.remove_depleted_tags()

    def on_node_captured(self, node):
        for tag in self:
            tag.on_node_captured(node)
        self.remove_depleted_tags()

    def on_turn_end_node(self, node):
        for tag in self:
            tag.on_turn_end_node(node)
        self.remove_depleted_tags()

    def on_turn_end_player(self, player):
        for tag in self:
            tag.on_turn_end_player(player)
        self.remove_depleted_tags()

    def on_turn_end_enemy(self, enemy):
        for tag in self:
            tag.on_turn_end_player(enemy)
        self.remove_depleted_tags()

    def on_turn_end_vector(self, vector, node):
        for tag in self:
            tag.on_turn_end_vector(vector, node)
        self.remove_depleted_tags()

    def on_turn_start_player(self, player):
        for tag in self:
            tag.on_turn_start_player(player)
        self.remove_depleted_tags()

    def on_vector_install(self, node, vector, player_info):
        for tag in self:
            tag.on_vector_install(node, vector, player_info)
        self.remove_depleted_tags()

    def on_script_execution(self, script):
        for tag in self:
            tag.on_script_execution(script)
        self.remove_depleted_tags()

    def on_temp_card_creation(self, card, player_info):
        for tag in self:
            tag.on_temp_card_creation(card, player_info)
        self.remove_depleted_tags()
