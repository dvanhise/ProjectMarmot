import pygame
import logging
from src.game import Game
from src.game_state import get_game_state
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT


LOG_FILE = 'output.log'

def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    # Fix windows encoding issue in the log file - "bush hid the facts" bug
    with open(LOG_FILE, 'ab') as f:
        f.write(u'\uFEFF'.encode('UTF-8'))

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game = Game(screen, clock)
    get_game_state(game)  # First instantion must be with 'game' object argument
    game.load_game()

    running = True
    while running:
        game.level_update()
        game.check_events()
        running = game.render_screen()
    pygame.quit()


if __name__ == '__main__':
    main()
