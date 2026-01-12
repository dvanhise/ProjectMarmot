import pygame
from game_objects.card import Card
from game_objects.game_state import GameState
from game_objects.level import Level
from game_objects.level_definitions.level1 import definition as level1_def

from render.hand import generate as gen_hand
from render.script_builder import generate as gen_script
from render.board import generate as gen_board
from render.card import CARD_HEIGHT
from render.constants import *

from game_objects.card_definitions.registry import get_new_card


game = GameState()

# TODO: Add starter cards

game.deck.add_card(get_new_card('payload1'))
game.deck.add_card(get_new_card('payload1'))
game.deck.add_card(get_new_card('payload1'))
game.deck.add_card(get_new_card('payload1'))
game.deck.add_card(get_new_card('payload1'))
game.deck.add_card(get_new_card('payload1'))
game.deck.add_card(get_new_card('payload1'))
game.deck.add_card(get_new_card('payload1'))
game.deck.add_card(get_new_card('payload1'))
game.start_new_level(Level(*level1_def))


# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True


while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # Window X clicked
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # Render the board
    board_render = gen_board(game.level)
    screen.blit(board_render, (10, 10))

    # Render hand
    hand_render = gen_hand(game.deck)
    screen.blit(hand_render, (300, SCREEN_HEIGHT - CARD_HEIGHT - 10))

    # Render draw deck and discard pile

    # Render other buttons

    # Render script builder
    script_render = gen_script(game.script_builder)
    screen.blit(script_render, (400, 460))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(30)  # limits FPS to 30

pygame.quit()


# Modes:
# player wait
# player dragging card
# route select
# enemy acts
# enemy plans
