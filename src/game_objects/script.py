import logging
from game_objects.card import Card
from game_objects.card_type import CardType
from game_objects.vector import Vector


class Script:
    def __init__(self):
        self.power = 0
        self.vector = None  # TODO: Allow for multiple vectors
        self.boosts = []
        self.current_node = None


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
        self.payload_slots = 1
        self.mod_slots = 1
        self.vector_slots = 1
        self.slots = [ScriptSlot(CardType.SCRIPT_PAYLOAD), ScriptSlot(CardType.SCRIPT_MOD), ScriptSlot(CardType.SCRIPT_VECTOR)]

    def clear(self):
        for slot in self.slots:
            slot.reset()

    def is_valid_play(self, card: Card, slot_ndx):
        return self.slots[slot_ndx].type == card.type

    def add_card(self, card_id: int, card: Card,  slot_ndx=0):
        replaced = self.slots[slot_ndx].set_card(card_id, card)
        return replaced

    def build_script(self):
        script = Script()
        for slot in self.slots:
            if slot.card.vector:
                self.vector = slot.card.vector
            if slot.card.on_script_activation:
                slot.card.on_script_activation(script)

        return script
