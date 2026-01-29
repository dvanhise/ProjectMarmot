import logging
from game_objects.player import Player
from game_objects.enemy import Enemy
from game_objects.script import ScriptBuilder
from game_objects.level import Level
from game_objects.level_definitions.level1 import definition as level1_def
from game_objects.level_definitions.level2 import definition as level2_def
from game_objects.route import Route
from game_objects.card_type import CardType

from render.hand import render_hand
from render.script_builder import render_script_builder
from render.network import render_network
from render.card import CARD_WIDTH, CARD_HEIGHT, generate as gen_card
from render.deck_info import render_deck_info
from render.end_turn_button import render_end_turn
from render.playzone import render_playzone
from render.energy_tracker import render_energy_tracker
from render.info_section import render_enemy_info, render_player_info
from render.terminal import render_terminal
from render.card_pick import render_card_pick
from render.help_text import render_help_text
from constants import *

from utils.image_loader import img_fetch
from utils.mouse_check import MouseCheck
from utils.card_registry import get_new_card, random_card_choices

from game_state import GameState


class Game:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock
        self.level = None
        self.mouse_check = MouseCheck()
        self.mouseover_text = None
        self.click_down = None

        self.player_route = None
        self.enemy_temp_route = None  # Pre-planned route of enemy
        self.enemy_route = None  # Route when running enemy script
        self.card_choices = []

        # Preload
        self.background = pygame.transform.smoothscale(img_fetch().get('background'), (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.level_ndx = 0
        self.level_order = [level1_def, level2_def]


    def on_enter_state(self, event, state):
        logging.info(f"Entering '{state.id}' state from '{event}' event.")

    def after_pre_turn_prep_complete(self):
        self.player.start_turn()

    def after_end_turn(self):
        self.player.end_turn()

    def after_enemy_script_complete(self):
        self.enemy.script = None
        self.enemy_temp_route = None
        self.enemy_route = None

    def after_player_script_complete(self):
        self.player.script = None
        self.player_route = None
        self.player.discard_pile += self.script_builder.clear()

    def on_exit_end_of_level(self):
        self.level_ndx += 1

    def on_enter_card_pick(self):
        self.card_choices = random_card_choices(self.player.card_reward_count)

    def before_hardware_pick(self):
        pass

    def player_lost_level(self):
        return self.player.check_defeat()

    def player_won_level(self):
        return self.enemy.check_defeat()

    def player_won_game(self):
        return self.level_ndx > len(self.level_order)

    def on_enter_game_end_loss(self):
        logging.info('YOU LOSE')

    def on_enter_game_end_win(self):
        logging.info('YOU WIN')

    def load_game(self):
        self.player = Player()
        self.script_builder = ScriptBuilder()

        # Starter deck
        self.player.add_card(get_new_card('spike'))
        self.player.add_card(get_new_card('spike'))
        self.player.add_card(get_new_card('spike'))
        self.player.add_card(get_new_card('spike'))
        self.player.add_card(get_new_card('amplifier'))
        self.player.add_card(get_new_card('amplifier'))
        self.player.add_card(get_new_card('security-group'))
        self.player.add_card(get_new_card('security-group'))
        self.player.add_card(get_new_card('query'))


    def level_update(self):
        # Load new level
        if get_state() == GameState.setup_level:
            self.level = Level(self.level_order[self.level_ndx])
            self.enemy = Enemy(self.level_order[self.level_ndx])
            self.script_builder.clear()
            self.player.reset()
            change_state('setup_level_complete')

        elif get_state() == GameState.pre_turn_prep:
            self.enemy_temp_route = Route(self.level.get_source('ENEMY'), 'ENEMY')
            self.enemy_temp_route.generate_path('RANDOM')
            self.enemy.next_script()
            change_state('pre_turn_prep_complete')

            # Card status right before player turn
            # logging.info(self.player.current_hand)
            # logging.info(self.player.draw_pile)
            # logging.info(self.player.discard_pile)

        elif get_state() == GameState.run_enemy_script:
            if not self.enemy_route:
                self.enemy_route = Route(self.level.get_source('ENEMY'), 'ENEMY')
                return
            pygame.time.wait(1500)  # Delay enemy action for clarity

            self.enemy_route.choose_next_node_from_route(self.enemy_temp_route)
            success = self.enemy.script.on_node_advance(self.enemy_route.edge_path[-1], self.enemy_route.node_path[-1], self.player, autoplay_vector=True)
            if not success or self.enemy_route.is_path_complete():
                change_state('enemy_script_complete')

        elif get_state() == GameState.end_of_level:
            # Placeholder state for end of a level
            pygame.time.wait(1500)
            change_state('end_of_level_progress')

    def check_events(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_on = self.mouse_check.on_interactable_object(mouse_x, mouse_y)

        self.mouseover_text = self.mouse_check.on_mouseover_object(mouse_x, mouse_y)

        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Window X clicked
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if get_state() == GameState.wait_for_player:
                    if mouse_on in ['SEND_SCRIPT', 'END_TURN']:
                        self.click_down = mouse_on
                    elif mouse_on.startswith('CARD'):
                        card_id = self.player.current_hand[int(mouse_on.replace('CARD', ''))]
                        self.player.start_drag(card_id)
                        change_state('start_drag')

                elif get_state() == GameState.card_pick and (mouse_on == 'NEXT_BUTTON' or mouse_on.startswith('PICK_CARD')):
                    self.click_down = mouse_on
                elif get_state() == GameState.run_player_script and (mouse_on.startswith('NODE') or mouse_on.startswith('INSTALL_VECTOR')):
                    self.click_down = mouse_on

                elif get_state() == GameState.game_end_loss:
                    # quit game
                    pass
                elif get_state() == GameState.game_end_win:
                    # quit game
                    pass


            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if get_state() == GameState.wait_for_player:
                    if mouse_on == 'END_TURN' and self.click_down == 'END_TURN':
                        change_state('end_turn')
                    elif mouse_on == 'SEND_SCRIPT' and self.click_down == 'SEND_SCRIPT':
                        self.send_script()

                if get_state() == GameState.card_drag:
                    card = self.player.get_dragged_card()
                    if mouse_on.startswith('SCRIPT'):
                        ndx = int(mouse_on.replace('SCRIPT', ''))
                        self.play_card_on_script_builder(ndx, card)
                    elif mouse_on.startswith('NODE'):
                        node_id = int(mouse_on.replace('NODE', ''))
                        node = self.level.nodes[node_id]
                        self.play_card_on_node(node, card)
                    elif mouse_on == 'PLAYZONE':
                        self.play_generic_card(card)
                    else:
                        self.player.add_card_to_hand(self.player.dragged)  # Card drop in invalid location
                    logging.info(f'No longer dragging "{self.player.dragged}"')
                    self.player.dragged = None
                    change_state('card_drop')

                elif get_state() == GameState.run_player_script:
                    if mouse_on.startswith('NODE') and self.click_down == mouse_on:
                        # Select the next node in the path
                        self.node_selected(mouse_on)
                    if mouse_on.startswith('INSTALL_VECTOR') and self.click_down == mouse_on:
                        vector_ndx = int(mouse_on.replace('INSTALL_VECTOR', ''))
                        self.player_route.node_path[-1].install_vector(self.player.script.vector.pop(vector_ndx))

                elif get_state() == GameState.card_pick:
                    if mouse_on.startswith('PICK_CARD') and self.click_down == mouse_on:
                        pick_card_ndx = int(mouse_on.replace('PICK_CARD', ''))
                        self.player.add_card(self.card_choices.pop(pick_card_ndx))
                    elif mouse_on == 'NEXT_BUTTON' and self.click_down == mouse_on:
                        change_state('end_of_level_progress')
                elif get_state() == GameState.game_end_loss:
                    pass
                elif get_state() == GameState.game_end_win:
                    pass

                self.click_down = None

    def render_screen(self):
        # Clear screen from last frame
        self.screen.fill("black")
        self.screen.blit(self.background, (0, 0))

        self.mouse_check.reset()

        # Render the network
        if get_state() == GameState.run_enemy_script:
            render_network(self.screen, self.level, self.player.script, self.enemy.script, [self.enemy_route, self.player_route])
        else:
            interactables, mouseovers = render_network(self.screen, self.level, self.player.script, None, [self.enemy_temp_route, self.player_route])
            self.mouse_check.register_rect(interactables)
            self.mouse_check.register_mouseover_rect(mouseovers)

        # Render info
        render_player_info(self.screen, self.player)
        render_enemy_info(self.screen, self.enemy)
        render_terminal(self.screen, self.player)
        render_terminal(self.screen, self.enemy)

        # Render hand
        if len(self.player.current_hand):
            interactables = render_hand(self.screen, self.player)
            self.mouse_check.register_rect(interactables)

        # Render card counts in draw and discard
        interactables = render_deck_info(self.screen, self.player)
        self.mouse_check.register_rect(interactables)

        # Render end turn button
        interactables = render_end_turn(self.screen)
        self.mouse_check.register_rect(interactables)

        # Render script builder
        interactables = render_script_builder(self.screen, self.script_builder)
        self.mouse_check.register_rect(interactables)

        # Render zone to play non-specific cards
        interactables = render_playzone(self.screen)
        self.mouse_check.register_rect(interactables)

        # Render current energy
        render_energy_tracker(self.screen, self.player)

        # Render card pick screen
        if get_state() == GameState.card_pick:
            interactables = render_card_pick(self.screen, self.card_choices)
            self.mouse_check.register_rect(interactables)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Render mouseover text
        if self.mouseover_text:
            render_help_text(self.screen, self.mouseover_text, mouse_x, mouse_y)
        self.mouseover_text = None

        # Render dragged card to mouse position
        if get_state() == GameState.card_drag and self.player.dragged:
            self.screen.blit(
                gen_card(self.player.get_dragged_card()),
                (mouse_x - CARD_WIDTH//2, mouse_y - CARD_HEIGHT//2)
            )

        # Render version
        font = pygame.font.SysFont("assets/fonts/BrassMono-Regular.ttf", 30)
        text = font.render(DEVELOPMENT_VERSION, True, 'white')
        self.screen.blit(text, (2, 2))

        pygame.display.flip()  # Displays changed on screen

        self.clock.tick(30)  # limits FPS to 30

        return True

    def node_selected(self, selection_id):
        node_id = int(selection_id.replace('NODE', ''))
        node = self.level.nodes[node_id]
        if node not in self.player_route.get_next_node_options():
            logging.warning(f'Selected node "{node.id}" not an option for next node.')
            return

        self.player_route.choose_next_node(node)
        success = self.player.script.on_node_advance(self.player_route.edge_path[-1], self.player_route.node_path[-1], self.level)

        if not success or self.player_route.is_path_complete():
            change_state('player_script_complete')

    def send_script(self):
        if not self.player.has_energy(1):
            logging.info(f'Not enough energy to execute script.')
            return

        self.player.pay_energy(1)
        self.player.script = self.script_builder.build_script()
        self.player_route = Route(self.level.get_source('PLAYER'), 'PLAYER')
        self.player.script.on_node_advance(None, self.player_route.node_path[-1], self.level)
        change_state('send_script_selected')

    def play_card_on_node(self, node, card):
        if card.type != CardType.WARD:
            logging.info(f'Invalid card type.  Expected "{CardType.WARD}", received "{card.type}".')
            self.player.add_card_to_hand(self.player.dragged)
        elif not self.player.has_energy(card.cost):
            logging.info(f'Not enough energy to play card.  Player has "{self.player.energy}", requires "{card.cost}".')
            self.player.add_card_to_hand(self.player.dragged)
        elif node.owner != 'PLAYER':
            logging.info(f'Invalid target node owned by "{node.owner}".')
            self.player.add_card_to_hand(self.player.dragged)
        else:
            self.player.pay_energy(card.cost)
            node.apply_ward_from_card(card)


    def play_card_on_script_builder(self, script_ndx, card):
        if not self.script_builder.is_valid_play(card, script_ndx):
            logging.info(f'Invalid card type.  Expected "{self.script_builder.slots[script_ndx].type}", received "{card.type}"')
            self.player.add_card_to_hand(self.player.dragged)
        elif not self.player.has_energy(card.cost):
            logging.info(f'Not enough energy to play card.  Player has "{self.player.energy}", requires "{card.cost}".')
            self.player.add_card_to_hand(self.player.dragged)
        else:
            self.player.pay_energy(card.cost)
            replaced = self.script_builder.add_card(self.player.dragged, card, script_ndx)
            if replaced:
                self.player.add_card_to_discard(replaced)

    def play_generic_card(self, card):
        if card.type != CardType.UTILITY:
            logging.info(f'Invalid card type.  Expected "{CardType.UTILITY}", received "{card.type}".')
            self.player.add_card_to_hand(self.player.dragged)
        elif not self.player.has_energy(card.cost):
            logging.info(f'Not enough energy to play card.  Player has "{self.player.energy}", requires "{card.cost}".')
            self.player.add_card_to_hand(self.player.dragged)
        else:
            self.player.pay_energy(card.cost)
            self.player.play_card_generic(self.player.dragged)


# Hacky workaround to allow the Game class to modify GameState and define on-change methods
game_state = None

def change_state(new_state):
    global game_state
    game_state.send(new_state)

def get_state():
    global game_state
    return game_state.current_state


def main():
    logging.getLogger().setLevel(logging.DEBUG)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game = Game(screen, clock)
    
    global game_state
    game_state = GameState(game)
    game.load_game()
    change_state('loading_complete')

    running = True
    while running:
        game.level_update()
        game.check_events()
        running = game.render_screen()
    pygame.quit()


if __name__ == '__main__':
    main()
