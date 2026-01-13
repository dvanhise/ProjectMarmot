from game_objects.card import Card
from game_objects.vector import Vector
import logging


class Script:
    def __init__(self):
        self.power = 0
        self.vector = None  # TODO: Allow for multiple vectors
        self.boosts = []

class ScriptBuilder:
    def __init__(self):
        self.payload_slots = 1
        self.mod_slots = 1
        self.vector_slots = 1
        self.clear()

    def clear(self):
        self.payloads = []
        self.mods = []
        self.vectors = []

    def add_card(self, card: Card, slot_type, slot_ndx=0):
        if card.type != slot_type:
            logging.error(f'Incorrect card type.  "{card.type}" found, expected "{slot_type}"')
            return

        self.payloads[slot_ndx] = card

    def send_script(self):
        script = Script()
        for card in self.payloads + self.mods + self.vectors:
            if card.vector:
                self.vector = Vector(**card.vector)
            card.on_script_activation(script)

        self.clear()

        return script
