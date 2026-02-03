import pygame
from utils.text_helper import draw_text_with_outline
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, DARK_TERMINAL, TERMINAL_GREEN


INTRO_TEXT = """Hello... Again...
 
It's time to begin your quest to become the greatest hacker of all time.
You must go toe-to-toe with shady megacorps and other hackers trying to prove themselves.

Each level had a network of interconnected servers between the player and the enemy.
Nodes = The locations in the network
Edges = The connections between the nodes

Build scripts and execute them to send payloads across the network to take over nodes and go after the opponent's health.

Place payload, mod, and vector cards in the labeled script slots and send the script with the "Execute" button
    Note: A script can be sent with some or even all slots empty
    
Select nodes in network to direct the path of the script.
If the script includes a vector, select it to install it on the current node.

A script continues on until it runs out of power or gets to the enemy's primary node and damages their health.
Any nodes that a script makes it to are captured by the player.
Non-friendly edges, ones that aren't green, reduce the power of a script traveling through them.

Card types:

Utility
    - Played on the "Utility" slot
    - Take effect immediately.

Wards
    - Played on nodes controlled by the player
    - Applies ward (defense) and other effects to node.  Ward protects the node against enemy scripts.
    - Ward values replace existing ward on nodes if they are higher.  Ward is not usually additive.

Payloads
    - A component of scripts
    - Impact the script's power

Mods
    - A component of scripts
    - Have a variety of effects

Vectors
    - A component of scripts
    - Can be installed on nodes that script goes through
    - Buffs scripts that move through that node in the future
    
Dictionary:
tags = buffs/debuffs on nodes, vectors, and players
delete = exhaust in StS
"""


PADDING = 50
LINE_HEIGHT = 15
BUTTON_SIZE = (160, 40)


def render_intro_screen(s: pygame.Surface):
    # Background and Border
    pygame.draw.rect(s, DARK_TERMINAL, pygame.Rect(PADDING, PADDING, SCREEN_WIDTH-2*PADDING, SCREEN_HEIGHT-2*PADDING), border_radius=5)
    pygame.draw.rect(s, '#444444', pygame.Rect(PADDING, PADDING, SCREEN_WIDTH-2*PADDING, SCREEN_HEIGHT-2*PADDING), width=5, border_radius=5)
    pygame.draw.rect(s, '#CCCCCC', pygame.Rect(PADDING, PADDING, SCREEN_WIDTH-2*PADDING, SCREEN_HEIGHT-2*PADDING), width=2, border_radius=5)

    font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', 14)
    for ndx, line in enumerate(INTRO_TEXT.split('\n')):
        text = font.render(line, True, TERMINAL_GREEN)
        text_rect = text.get_rect(topleft=(PADDING+20, PADDING+20+ndx*LINE_HEIGHT))
        s.blit(text, text_rect)

    button_rect = pygame.Rect((PADDING+20, SCREEN_HEIGHT-PADDING-20-BUTTON_SIZE[1]), BUTTON_SIZE)
    pygame.draw.rect(s, '#5CC9D4', button_rect)
    pygame.draw.rect(s, '#444444', button_rect, width=2)
    font = pygame.font.Font('assets/fonts/BrassMono-Regular.ttf', 20)
    outline_text = draw_text_with_outline('Start', font, 'white', 2, 'black')
    text_rect = outline_text.get_rect(center=(PADDING+20+BUTTON_SIZE[0]//2, SCREEN_HEIGHT-PADDING-20-BUTTON_SIZE[1]//2))
    s.blit(outline_text, text_rect)

    return {'START_BUTTON': button_rect}
