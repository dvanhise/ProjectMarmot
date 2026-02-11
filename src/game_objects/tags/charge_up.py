from src.game_objects.tag import Tag
from src.game_objects.tags.boost import Boost
from src.utils.action_queue import get_aq


class ChargeUp(Tag):
    id = 'charge-up'
    name = 'Charge Up'
    icon = 'power'
    tooltip = 'On vector install, use all energy(X), gain {count+1}*X Boost.'

    def on_vector_install(self, node, vector, player_info):
        energy = player_info['energy']
        vector.tags.add_tag(Boost(energy*(self.count + 1)))
        get_aq().queue_action('change_energy', -energy)
