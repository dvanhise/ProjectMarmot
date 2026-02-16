import logging
import copy
from src.game_objects.card import Card
from src.game_objects.card_type import CardType
from src.game_objects.graph import Edge, Node
from src.game_objects.tag import TagManager


class Script:
    def __init__(self, owner):
        self.owner = owner
        self.power = 0
        self.pathing = None
        self.vector = []
        self.tags = TagManager()

        # Properties that should be tags, but it's easier to put them here
        self.destroy_vector_on_capture = True
        self.edge_difficulty_reduction = 0

    def on_node_advance(self, edge: Edge, node: Node, opponent, autoplay_vector = False):
        # 'edge' can be None if approaching the source node
        # Return True if script is still running, return False if it was defeated

        # Interact with edge
        if edge and self.owner != edge.owner:
            self.power -= max(0, edge.difficulty - self.edge_difficulty_reduction)

            if self.power <= 0:
                return False

        # Interact with ward
        if self.owner != node.owner:

            # Before interaction with ward
            self.tags.before_ward_encounter_as_script(self, node)
            node.tags.before_ward_encounter_as_node(self, node)
            if node.vector:
                node.vector.tags.before_ward_encounter_as_vector(self, node)

            if node.ward >= self.power:
                node.ward -= self.power

                self.tags.on_failed_node_encounter_as_script(self, node)
                node.tags.on_failed_node_encounter_as_node(self, node)
                if node.vector:
                    node.vector.tags.on_failed_node_encounter_as_vector(self, node)

                return False
            else:
                self.power -= node.ward
                node.ward = 0

        # Before interaction with node
        self.tags.before_node_encounter_as_script(self, node)
        node.tags.before_node_encounter_as_node(self, node)
        if node.vector:
            node.vector.tags.before_node_encounter_as_vector(self, node)

        if self.power < 0:
            # A script can fail here due to tags like Fortify
            self.tags.on_failed_node_encounter_as_script(self, node)
            node.tags.on_failed_node_encounter_as_node(self, node)
            if node.vector:
                node.vector.tags.on_failed_node_encounter_as_vector(self, node)
            return False

        # Interact with captured unfriendly node
        if self.owner != node.owner:
            self.tags.on_node_capture_as_script(self, node)
            node.tags.on_node_capture_as_node(self, node)
            if node.vector:
                node.vector.tags.on_node_capture_as_vector(self, node)

            if self.destroy_vector_on_capture:
                node.vector = None

            if node.source:
                opponent.change_health(-self.power)
            else:
                node.owner = self.owner

                # Update edge ownership after node ownership changes
                for e in node.right + node.left:
                    if e.left.owner == e.right.owner:
                        e.owner = e.left.owner
                    else:
                        e.owner = 'NEUTRAL'

        # Interaction with friendly node
        else:
            self.tags.on_friendly_node_encounter_as_script(self, node)
            node.tags.on_friendly_node_encounter_as_node(self, node)
            if node.vector:
                node.vector.tags.on_friendly_node_encounter_as_vector(self, node)

        # Automatically install enemy vector if node doesn't have one installed
        if autoplay_vector and len(self.vector) and not node.vector:
            node.install_vector(self.vector.pop(0))
            node.vector.tags.on_vector_install(node, node.vector, {})  # TODO: Add enemy info if ever needed

        return True


class ScriptSlot:
    def __init__(self, slot_type: CardType, temporary: bool = False):
        self.type = slot_type
        self.temp = temporary
        self.card = None
        self.card_id = None

    def set_card(self, card_id, card):
        old_card_id = self.card_id
        self.card = card
        self.card_id = card_id

        return old_card_id

    def reset(self):
        old_card_id = self.card_id
        self.card = None
        self.card_id = None

        return old_card_id


class ScriptBuilder:
    MAX_SLOTS = 6

    def __init__(self):
        self.slots = [ScriptSlot(CardType.SCRIPT_PAYLOAD), ScriptSlot(CardType.SCRIPT_MOD), ScriptSlot(CardType.SCRIPT_VECTOR)]

    def init_round(self):
        # Clear out temporary slots
        self.slots = [slot for slot in self.slots if not slot.temp]

    def add_slot(self, card_type, temporary=False):
        if len(self.slots) >= self.MAX_SLOTS:
            logging.warning(f'Unable to add script slot.  Currently at {len(self.slots)}/{self.MAX_SLOTS} slots.')
            return

        new_slot = ScriptSlot(card_type, temporary)
        loc = next(ndx for ndx, slot in enumerate(self.slots) if slot.type==card_type)
        self.slots = self.slots[0:loc+1] + [new_slot] + self.slots[loc+1:]

    def clear(self):
        return [slot.reset() for slot in self.slots if slot.card_id is not None]

    def is_valid_play(self, card: Card, slot_ndx):
        return self.slots[slot_ndx].type == card.type

    def add_card(self, card_id: int, card: Card,  slot_ndx=0):
        replaced = self.slots[slot_ndx].set_card(card_id, card)
        return replaced

    def build_script(self, player_info):
        script = Script('PLAYER')
        for slot in self.slots:
            if not slot.card:
                continue
            if slot.card.vector:
                script.vector.append(copy.deepcopy(slot.card.vector))
            if slot.card.on_script_activation:
                slot.card.on_script_activation(script, player_info)

        return script
