import pygame
import logging
from game_objects.player import Player
from game_objects.script import ScriptBuilder
from game_objects.level import Level
from game_objects.level_definitions.level1 import definition as level1_def

from render.hand import render_hand
from render.script_builder import render_script_builder
from render.network import render_network
from render.card import CARD_WIDTH, CARD_HEIGHT
from render.draw_pile import generate as gen_draw
from render.discard_pile import generate as gen_discard
from render.end_turn_button import render_end_turn
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
        self.click_check = ClickCheck()
        self.click_down = None

        # Preload
        self.background = pygame.transform.smoothscale(img_fetch().get('background'), (SCREEN_WIDTH, SCREEN_HEIGHT))

    def load_game(self):
        self.player = Player()
        self.script_builder = ScriptBuilder()
        self.level = Level(level1_def)
        self.script_builder.clear()

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

        self.player.reset()
        self.player.draw(5)


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
                        # Figure out which card
                        # start card drag
                        pass

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
                        self.state.end_turn()
                    elif mouse_on == 'SEND_SCRIPT' and self.click_down == 'SEND_SCRIPT':
                        self.state.send_script()
                if self.state.current_state == GameState.card_drag:
                    if mouse_on.startswith('SCRIPT'):
                        ndx = int(mouse_on.replace('SCRIPT', ''))
                        # Add or replace script space if valid
                        pass
                    elif mouse_on.startswith('NODE') and self.click_down == mouse_on:
                        # Play card on node if valid
                        pass
                    elif mouse_on.startswith('UTILITY_PLAY_AREA_TODO'):
                        # Play card if valid
                        pass
                    else:
                        # Card drop invalid, put back in hand
                        pass
                elif self.state.current_state == GameState.choose_script_path:
                    if mouse_on.startswith('NODE') and self.click_down == mouse_on:
                        # Play card on node if valid
                        pass
                    pass
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
        interactables = render_network(self.screen, self.level)
        self.click_check.register_rect(interactables)

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

        # Render dragged card
        if self.state.card_drag:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            c = self.player.dragged

        # Render current energy
        # Render current health

        # Render version
        font = pygame.font.SysFont("assets/fonts/BrassMono-Regular.ttf", 30)
        text = font.render(DEVELOPMENT_VERSION, True, 'white')
        self.screen.blit(text, (2, 2))

        # flip() the display to put your work on screen
        pygame.display.flip()

        self.clock.tick(30)  # limits FPS to 30

        return True


def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game = Game(screen, clock)
    game.load_game()
    game.state.loading_complete()

    running = True
    while running:
        game.check_events()
        game.render_screen()
    pygame.quit()


if __name__ == '__main__':
    main()
