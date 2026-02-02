from game_objects.script import Script
from game_objects.tags.energy_drain import EnergyDrain
from game_objects.card_type import CardType
from game_objects.card import Card


class RemoteMiner(Card):
    id = 'remote-miner'
    name = 'Remote Miner'
    type = CardType.SCRIPT_MOD
    rarity = 'intermediate'
    image_id = 'mod',
    cost = 2
    description = ['Gain 1 energy for', 'each node captured']

    def on_script_activation(self, script: Script, player_info):
        script.tags.append(EnergyDrain(1))
