from src.game_objects.script import Script
from src.game_objects.tags.energy_drain import EnergyDrain
from src.game_objects.card_type import CardType
from src.game_objects.card import Card


class RemoteMiner(Card):
    id = 'remote-miner'
    name = 'Remote Miner'
    type = CardType.SCRIPT_MOD
    rarity = 'intermediate'
    image_id = 'mod'
    cost = 1
    description = ['Gain 1 energy for', 'each node captured']

    def on_script_activation(self, script: Script, player_info):
        script.tags.add_tag(EnergyDrain(1))
