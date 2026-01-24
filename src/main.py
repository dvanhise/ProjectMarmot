import logging
from game_objects.player import Player
from game_objects.script import ScriptBuilder
from game_objects.level import Level
from game_objects.level_definitions.level1 import definition as level1_def
from game_objects.route import Route
from game_objects.card_type import CardType

from render.hand import render_hand
from render.script_builder import render_script_builder
from render.network import render_network
from render.card import CARD_WIDTH, CARD_HEIGHT, generate as gen_card
from render.draw_pile import generate as gen_draw
from render.discard_pile import generate as gen_discard
from render.end_turn_button import render_end_turn
from render.playzone import render_playzone
from render.energy_tracker import render_energy_tracker
from render.info_section import render_enemy_info, render_player_info
from constants import *

from utils.image_loader import img_fetch
from utils.click_check import ClickCheck
from utils.card_registry import get_new_card

from game_state import GameState


class Game:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock
        self.state = GameState()
        self.level = None
        self.click_check = ClickCheck()
        self.click_down = None

        self.player_route = None
        self.enemy_route = None
        self.player_script = None
        self.enemy_script = None

        # Preload
        self.background = pygame.transform.smoothscale(img_fetch().get('background'), (SCREEN_WIDTH, SCREEN_HEIGHT))

    def load_game(self):
        self.player = Player()
        self.script_builder = ScriptBuilder()

        # Starter deck
        self.player.add_card(get_new_card('basic-payload'))
        self.player.add_card(get_new_card('basic-payload'))
        self.player.add_card(get_new_card('basic-payload'))
        self.player.add_card(get_new_card('basic-payload'))
        self.player.add_card(get_new_card('basic-mod'))
        self.player.add_card(get_new_card('basic-vector'))
        self.player.add_card(get_new_card('basic-vector'))
        self.player.add_card(get_new_card('basic-ward'))
        self.player.add_card(get_new_card('basic-ward'))
        self.player.add_card(get_new_card('basic-utility'))


    def level_update(self):
        # Load new level
        if self.state.current_state == GameState.setup_level:
            self.level = Level(level1_def)
            self.script_builder.clear()
            self.state.setup_level_complete()
            self.player.reset()
            self.player.start_turn()

        elif self.state.current_state == GameState.plan_enemy_turn:
            self.enemy_route = Route(self.level.get_source('ENEMY'), 'ENEMY')
            self.enemy_route.generate_path('RANDOM')
            self.enemy_script = self.level.next_script()
            self.state.plan_enemy_turn_complete()

        elif self.state.current_state == GameState.enemy_turn:
            pygame.time.wait(2000)  # Delay enemy action for clarity
            edge, node = self.enemy_route.next()
            success = self.enemy_script.on_node_advance(edge, node, self.player)

            if self.player.check_loss():
                self.state.script_level_loss()
                self.enemy_script = None
                self.enemy_route = None
            elif not success or self.enemy_route.is_path_complete():
                self.state.script_complete()
                self.enemy_script = None
                self.enemy_route = None

    def check_events(self):
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Window X clicked
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_on = self.click_check.on_object(mouse_x, mouse_y)

                if self.state.current_state == GameState.wait_for_player:
                    if mouse_on in ['SEND_SCRIPT', 'END_TURN']:
                        self.click_down = mouse_on
                    elif mouse_on.startswith('CARD'):
                        card_id = self.player.current_hand[int(mouse_on.replace('CARD', ''))]
                        self.player.start_drag(card_id)
                        self.state.start_drag()

                elif self.state.current_state == GameState.evaluate_script:
                    if mouse_on.startswith('NODE') or mouse_on.startswith('INSTALL_VECTOR'):
                        self.click_down = mouse_on

                elif self.state.current_state == GameState.end_of_level:
                    # select card or next level
                    pass
                elif self.state.current_state == GameState.game_end_loss:
                    # quit game
                    pass
                elif self.state.current_state == GameState.game_end_win:
                    # quit game
                    pass


            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_on = self.click_check.on_object(mouse_x, mouse_y)

                if self.state.current_state == GameState.wait_for_player:
                    if mouse_on == 'END_TURN' and self.click_down == 'END_TURN':
                        self.player.end_turn()
                        self.state.end_turn()
                    elif mouse_on == 'SEND_SCRIPT' and self.click_down == 'SEND_SCRIPT':
                        # Player selected execute script.  Build and initiate the script
                        self.send_script()

                if self.state.current_state == GameState.card_drag:
                    card = self.player.get_dragged_card()
                    if mouse_on.startswith('SCRIPT'):
                        ndx = int(mouse_on.replace('SCRIPT', ''))
                        if self.script_builder.is_valid_play(card, ndx) and self.player.has_energy(card.cost):
                            self.player.pay_energy(card.cost)
                            replaced = self.script_builder.add_card(self.player.dragged, card, ndx)
                            if replaced:
                                self.player.add_card_to_discard(replaced)
                        else:
                            self.player.add_card_to_hand(self.player.dragged)
                    elif mouse_on.startswith('NODE'):
                        node_id = int(mouse_on.replace('NODE', ''))
                        node = self.level.nodes[node_id]
                        if card.type == CardType.WARD and self.player.has_energy(card.cost):
                            self.player.pay_energy(card.cost)
                            node.apply_ward()

                    elif mouse_on == 'PLAYZONE':
                        if card.type == CardType.UTILITY and self.player.has_energy(card.cost):
                            self.player.pay_energy(card.cost)
                            self.player.play_card_generic(self.player.dragged)
                    else:
                        # Card drop invalid, put back in hand
                        self.player.add_card_to_hand(self.player.dragged)
                    self.state.card_drop()
                    self.player.dragged = None

                elif self.state.current_state == GameState.evaluate_script:
                    if mouse_on.startswith('NODE') and self.click_down == mouse_on:
                        # Select the next node in the path
                        self.node_selected(mouse_on)
                    if mouse_on.startswith('INSTALL_VECTOR') and self.click_down == mouse_on:
                        vector_ndx = int(mouse_on.replace('INSTALL_VECTOR', ''))
                        self.player_route.node_path[-1].install_vector(self.player_script.vector.pop(vector_ndx))

                elif self.state.current_state == GameState.end_of_level:
                    pass
                elif self.state.current_state == GameState.game_end_loss:
                    pass
                elif self.state.current_state == GameState.game_end_win:
                    pass

                self.click_down = None

    def render_screen(self):
        # Clear screen from last frame
        self.screen.fill("black")
        self.screen.blit(self.background, (0, 0))

        self.click_check.reset()

        # Render the network
        interactables = render_network(self.screen, self.level, self.player_script, [self.enemy_route, self.player_route])
        self.click_check.register_rect(interactables)

        # Render info
        render_player_info(self.screen, self.player)
        render_enemy_info(self.screen, self.level)

        # Render scripts


        # Render hand
        interactables = render_hand(self.screen, self.player)
        self.click_check.register_rect(interactables)

        # Render draw pile
        draw_render = gen_draw(self.player)
        self.screen.blit(draw_render, (10, SCREEN_HEIGHT - CARD_HEIGHT-20))

        # Render discard pile
        discard_render = gen_discard(self.player)
        self.screen.blit(discard_render, (10, SCREEN_HEIGHT - CARD_HEIGHT//2 - 10))

        # Render end turn button
        interactables = render_end_turn(self.screen)
        self.click_check.register_rect(interactables)

        # Render script builder
        interactables = render_script_builder(self.screen, self.script_builder)
        self.click_check.register_rect(interactables)

        # Render dragged card to mouse position
        if self.state.card_drag and self.player.dragged:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.screen.blit(
                gen_card(self.player.get_dragged_card()),
                (mouse_x - CARD_WIDTH//2, mouse_y - CARD_HEIGHT//2)
            )

        # Render zone to play non-specific cards
        interactables = render_playzone(self.screen)
        self.click_check.register_rect(interactables)

        # Render current energy
        render_energy_tracker(self.screen, self.player)

        # Render version
        font = pygame.font.SysFont("assets/fonts/BrassMono-Regular.ttf", 30)
        text = font.render(DEVELOPMENT_VERSION, True, 'white')
        self.screen.blit(text, (2, 2))

        # flip() the display to put your work on screen
        pygame.display.flip()

        self.clock.tick(30)  # limits FPS to 30

        return True

    def node_selected(self, selection_id):
        node_id = int(selection_id.replace('NODE', ''))
        node = self.level.nodes[node_id]
        if node not in self.player_route.get_next_node_options():
            logging.warning(f'Selected node "{node.id}" not an option for next node.')
            return

        self.player_route.choose_next_node(node)
        success = self.player_script.on_node_advance(self.player_route.edge_path[-1], self.player_route.node_path[-1], self.level)

        if self.level.check_victory():
            self.state.script_level_win()
        elif not success or self.player_route.is_path_complete():
            self.state.script_complete()

        if self.level.check_victory() or not success or self.player_route.is_path_complete():
            self.player_script = None
            self.player_route = None
            self.player.discard_pile += self.script_builder.clear()

    def send_script(self):
        if not self.player.has_energy(1):
            logging.warning(f'Not enough energy to execute script.')
            return

        self.player.pay_energy(1)
        self.player_script = self.script_builder.build_script()
        self.player_route = Route(self.level.get_source('PLAYER'), 'PLAYER')
        self.player_script.on_node_advance(None, self.player_route.node_path[-1], self.level)
        self.state.send_script_selected()


def main():
    logging.getLogger().setLevel(logging.DEBUG)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game = Game(screen, clock)
    game.load_game()
    game.state.loading_complete()

    running = True
    while running:
        game.level_update()
        game.check_events()
        game.render_screen()
    pygame.quit()


if __name__ == '__main__':
    main()
