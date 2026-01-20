import pygame
import logging
from game_objects.player import Player
from game_objects.script import ScriptBuilder
from game_objects.level import Level
from game_objects.level_definitions.level1 import definition as level1_def
from game_objects.route import Route

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
from render.constants import *

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

        if self.state.current_state == GameState.plan_enemy_turn:
            self.enemy_route = Route(self.level.get_source('ENEMY'), 'ENEMY')
            self.enemy_route.generate_path('RANDOM')
            self.state.plan_enemy_turn_complete()


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

                elif self.state.current_state == GameState.choose_script_path:
                    if mouse_on.startswith('NODE'):
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
                        # Start planning a route for the script
                        self.player_route = Route(self.level.get_source('PLAYER'), 'PLAYER')
                        self.state.send_script_selected()

                if self.state.current_state == GameState.card_drag:
                    if mouse_on.startswith('SCRIPT'):
                        ndx = int(mouse_on.replace('SCRIPT', ''))
                        if self.script_builder.is_valid_play(self.player.get_dragged_card(), ndx):
                            replaced = self.script_builder.add_card(self.player.dragged, self.player.get_dragged_card(), ndx)
                            if replaced:
                                self.player.add_card_to_discard(replaced)
                        else:
                            self.player.add_card_to_hand(self.player.dragged)
                        self.state.card_drop()
                    elif mouse_on.startswith('NODE'):
                        # TODO
                        # Play card on node if valid
                        self.state.card_drop()
                    elif mouse_on == 'PLAYZONE':
                        self.player.play_card_generic(self.player.dragged)
                        self.state.card_drop()
                    else:
                        # Card drop invalid, put back in hand
                        self.player.add_card_to_hand(self.player.dragged)
                    self.player.dragged = None

                elif self.state.current_state == GameState.choose_script_path:
                    if mouse_on.startswith('NODE') and self.click_down == mouse_on:
                        node_id = int(mouse_on.replace('NODE', ''))
                        node = self.level.nodes[node_id]
                        if node in self.player_route.get_next_node_options():
                            self.player_route.choose_next_node(node)
                            if self.player_route.is_path_complete():
                                self.state.script_path_complete()
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
        interactables = render_network(self.screen, self.level, [self.enemy_route, self.player_route])
        self.click_check.register_rect(interactables)

        # Render info
        render_player_info(self.screen, self.player)
        render_enemy_info(self.screen, self.level)

        # Render hand
        interactables = render_hand(self.screen, self.player)
        self.click_check.register_rect(interactables)

        # Render draw pile
        draw_render = gen_draw(self.player)
        self.screen.blit(draw_render, (10, SCREEN_HEIGHT - CARD_HEIGHT - 10))

        # Render discard pile
        discard_render = gen_discard(self.player)
        self.screen.blit(discard_render, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - CARD_HEIGHT - 10))

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
