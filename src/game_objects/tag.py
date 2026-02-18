class Tag:
    id = ''
    name = 'TODO'
    icon = 'tag_placeholder'
    tooltip = 'TODO'
    count = 0
    owner = ''
    positive = True  # Whether the tag is good or bad for the node/vector/player it's applied to

    def __init__(self, count):
        self.count = count

    def get_tooltip(self):
        return f'{self.name}: {self.tooltip.format(count=self.count)}'

    def get_full_name(self):
        return f'{self.id}{self.count}'

    def on_change(self, change):
        # Any time a tag is modified
        pass

    def before_ward_encounter_as_script(self, script, node):
        # Only applies when approaching unfriendly nodes
        pass

    def before_ward_encounter_as_node(self, script, node):
        # Only applies when approaching unfriendly nodes
        pass

    def before_ward_encounter_as_vector(self, script, node):
        # Only applies when approaching unfriendly nodes
        pass

    def before_node_encounter_as_script(self, script, node):
        pass

    def before_node_encounter_as_node(self, script, node):
        pass

    def before_node_encounter_as_vector(self, script, node):
        pass

    def on_failed_node_encounter_as_script(self, script, node):
        pass

    def on_failed_node_encounter_as_node(self, script, node):
        pass

    def on_failed_node_encounter_as_vector(self, script, node):
        pass

    def on_node_capture_as_script(self, script, node):
        # When an player captures a non-friendly node
        pass

    def on_node_capture_as_node(self, script, node):
        # When an player captures a non-friendly node
        pass

    def on_node_capture_as_vector(self, script, node):
        # When an player captures a non-friendly node
        pass

    def on_friendly_node_encounter_as_script(self, script, node):
        pass

    def on_friendly_node_encounter_as_node(self, script, node):
        pass

    def on_friendly_node_encounter_as_vector(self, script, node):
        pass

    def on_vector_install_as_script(self, script, node, vector, player_info):
        pass

    def on_vector_install_as_node(self, script, node, vector, player_info):
        pass

    def on_vector_install_as_vector(self, script, node, vector, player_info):
        pass

    def on_turn_end_player(self, player):
        pass

    def on_turn_end_enemy(self, enemy):
        pass

    def on_turn_end_node(self, vector, node):
        # Applies to both nodes and vectors
        pass

    def on_turn_start_player(self, player):
        pass

    def on_script_creation(self, script):
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

    def before_ward_encounter_as_script(self, script, node):
        for tag in self:
            tag.before_ward_encounter_as_script(script, node)
        self.remove_depleted_tags()

    def before_ward_encounter_as_node(self, script, node):
        for tag in self:
            tag.before_ward_encounter_as_node(script, node)
        self.remove_depleted_tags()

    def before_ward_encounter_as_vector(self, script, node):
        for tag in self:
            tag.before_ward_encounter_as_vector(script, node)
        self.remove_depleted_tags()

    def before_node_encounter_as_script(self, script, node):
        for tag in self:
            tag.before_node_encounter_as_script(script, node)
        self.remove_depleted_tags()

    def before_node_encounter_as_node(self, script, node):
        for tag in self:
            tag.before_node_encounter_as_node(script, node)
        self.remove_depleted_tags()

    def before_node_encounter_as_vector(self, script, node):
        for tag in self:
            tag.before_node_encounter_as_vector(script, node)
        self.remove_depleted_tags()

    def on_failed_node_encounter_as_script(self, script, node):
        for tag in self:
            tag.on_failed_node_encounter_as_script(script, node)
        self.remove_depleted_tags()

    def on_failed_node_encounter_as_node(self, script, node):
        for tag in self:
            tag.on_failed_node_encounter_as_node(script, node)
        self.remove_depleted_tags()

    def on_failed_node_encounter_as_vector(self, script, node):
        for tag in self:
            tag.on_failed_node_encounter_as_vector(script, node)
        self.remove_depleted_tags()

    def on_node_capture_as_script(self, script, node):
        for tag in self:
            tag.on_node_capture_as_script(script, node)
        self.remove_depleted_tags()

    def on_node_capture_as_node(self, script, node):
        for tag in self:
            tag.on_node_capture_as_node(script, node)
        self.remove_depleted_tags()

    def on_node_capture_as_vector(self, script, node):
        for tag in self:
            tag.on_node_capture_as_vector(script, node)
        self.remove_depleted_tags()

    def on_friendly_node_encounter_as_script(self, script, node):
        for tag in self:
            tag.on_friendly_node_encounter_as_script(script, node)
        self.remove_depleted_tags()

    def on_friendly_node_encounter_as_node(self, script, node):
        for tag in self:
            tag.on_friendly_node_encounter_as_node(script, node)
        self.remove_depleted_tags()

    def on_friendly_node_encounter_as_vector(self, script, node):
        for tag in self:
            tag.on_friendly_node_encounter_as_vector(script, node)
        self.remove_depleted_tags()

    def on_turn_end_player(self, player):
        for tag in self:
            tag.on_turn_end_player(player)
        self.remove_depleted_tags()

    def on_turn_end_enemy(self, enemy):
        for tag in self:
            tag.on_turn_end_player(enemy)
        self.remove_depleted_tags()

    def on_turn_end_node(self, vector, node):
        for tag in self:
            tag.on_turn_end_node(vector, node)
        self.remove_depleted_tags()

    def on_turn_start_player(self, player):
        for tag in self:
            tag.on_turn_start_player(player)
        self.remove_depleted_tags()

    def on_vector_install_as_script(self, script, node, vector, player_info):
        for tag in self:
            tag.on_vector_install_as_script(script, node, vector, player_info)
        self.remove_depleted_tags()

    def on_vector_install_as_node(self, script, node, vector, player_info):
        for tag in self:
            tag.on_vector_install_as_node(script, node, vector, player_info)
        self.remove_depleted_tags()

    def on_vector_install_as_vector(self, script, node, vector, player_info):
        for tag in self:
            tag.on_vector_install_as_vector(script, node, vector, player_info)
        self.remove_depleted_tags()

    def on_script_creation(self, script):
        for tag in self:
            tag.on_script_creation(script)
        self.remove_depleted_tags()

    def on_temp_card_creation(self, card, player_info):
        for tag in self:
            tag.on_temp_card_creation(card, player_info)
        self.remove_depleted_tags()
