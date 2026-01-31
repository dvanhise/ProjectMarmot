import logging
from game_objects.card import Card
from game_objects.card_type import CardType
from game_objects.graph import Edge, Node


class Script:
    def __init__(self, owner):
        self.owner = owner
        self.power = 0
        self.vector = []
        self.tags = []

    def on_node_advance(self, edge: Edge, node: Node, opponent, autoplay_vector = False):
        # 'edge' can be None if approaching the source node
        # Return True if script is still running, return False if it was defeated

        # Interact with edge
        if edge and self.owner != edge.owner:
            self.power -= edge.difficulty

        if self.power < 0:
            return False

        for tag in node.tags:
            tag.before_script_node_encounter(self, node)

        # Interact with non-friendly node
        if self.owner != node.owner:
            if node.ward > self.power:
                node.ward -= self.power
                for tag in node.tags:
                    tag.after_failed_script_node_encounter(self, node)
                return False
            else:
                self.power -= node.ward
                node.ward = 0
                for tag in node.tags:
                    tag.on_node_captured(node)
                    tag.after_successful_script_node_encounter(self, node)

            node.vector = None
            if node.source:
                # TODO: Vector effects
                opponent.change_health(-self.power)

            else:
                node.owner = self.owner

                # Update edge ownership after node ownership changes
                for e in node.right + node.left:
                    if e.left.owner == e.right.owner:
                        e.owner = e.left.owner
                    else:
                        e.owner = 'NEUTRAL'

        # Interact with friendly node
        elif node.vector:
            for tag in node.vector.tags:
                tag.on_friendly_script_node_encounter(self, node)

        # Automatically install a vector if node doesn't have one installed
        if autoplay_vector and len(self.vector) and not node.vector:
            node.install_vector(self.vector.pop(-1))

        return True


class ScriptSlot:
    def __init__(self, slot_type: CardType):
        self.type = slot_type
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
    def __init__(self):
        self.slots = [ScriptSlot(CardType.SCRIPT_PAYLOAD), ScriptSlot(CardType.SCRIPT_MOD), ScriptSlot(CardType.SCRIPT_VECTOR)]

    def clear(self):
        return [slot.reset() for slot in self.slots if slot.card_id]

    def is_valid_play(self, card: Card, slot_ndx):
        return self.slots[slot_ndx].type == card.type

    def add_card(self, card_id: int, card: Card,  slot_ndx=0):
        replaced = self.slots[slot_ndx].set_card(card_id, card)
        return replaced

    def build_script(self):
        script = Script('PLAYER')
        for slot in self.slots:
            if not slot.card:
                continue
            if slot.card.vector:
                script.vector.append(slot.card.vector)
            if slot.card.on_script_activation:
                slot.card.on_script_activation(script)

        return script
