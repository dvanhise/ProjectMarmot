import pygame
from game_objects.player import Player
from game_objects.script import ScriptBuilder
from game_objects.level import Level
from game_objects.level_definitions.level1 import definition as level1_def
from game_objects.card_definitions.registry import get_new_card

from render.hand import generate as gen_hand
from render.script_builder import generate as gen_script
from render.network import generate as gen_network
from render.card import CARD_HEIGHT
from render.constants import *

from game_state import GameState


class Game:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock
        self.state = GameState()

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

                if self.state.current_state == GameState.wait_for_player:
                    # start card drag, send script, or end turn
                    pass
                elif self.state.current_state == GameState.choose_script_path:
                    # select next node
                    pass
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
                if self.state.current_state == GameState.wait_for_player:
                    # card drop, send script, or end turn
                    pass
                elif self.state.current_state == GameState.choose_script_path:
                    # start select next node
                    pass
                elif self.state.current_state == GameState.end_of_level:
                    pass
                elif self.state.current_state == GameState.game_end_loss:
                    pass
                elif self.state.current_state == GameState.game_end_win:
                    pass

    def render_screen(self):

        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill("black")

        # Render the network
        network_render = gen_network(self.level)
        self.screen.blit(network_render, (10, 10))

        # Render hand
        hand_render = gen_hand(self.player)
        self.screen.blit(hand_render, (300, SCREEN_HEIGHT - CARD_HEIGHT - 10))

        # Render draw player and discard pile

        # Render other buttons

        # Render script builder
        script_render = gen_script(self.script_builder)
        self.screen.blit(script_render, (400, 460))

        # Render version
        font = pygame.font.SysFont("assets/fonts/BrassMono-Regular.ttf", 30)
        text = font.render("v0.1 Alpha", True, 'white')
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
