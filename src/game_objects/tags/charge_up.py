from src.game_objects.tag import Tag
from src.game_objects.tags.boost import Boost
from src.utils.action_queue import get_aq


class ChargeUp(Tag):
    id = 'charge-up'
    name = 'Charge Up'
    icon = 'tag_placeholder'
    tooltip = 'On vector install, use all energy(X), add {count}*X Boost.'

    def on_vector_install_as_vector(self, script, node, vector, player_info):
        energy = player_info['energy']
        vector.tags.add_tag(Boost(energy*self.count))
        get_aq().queue_action('change_energy', -energy)
        vector.tags.remove(self)
