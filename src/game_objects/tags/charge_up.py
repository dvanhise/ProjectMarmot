from game_objects.tag import Tag
from game_objects.tags.boost import Boost
from utils.action_queue import get_aq


class ChargeUp(Tag):
    id = 'charge-up'
    icon = 'power'
    tooltip = 'On vector install, use all energy(X), gain {count+1}*X Boost.'

    def on_vector_install(self, node, vector, player_info):
        energy = player_info['energy']
        vector.tags.add_tag(Boost(energy*(self.count + 1)))
        get_aq().queue_action('change_energy', -energy)
