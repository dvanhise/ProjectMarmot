import logging
import random

import pygame

from src.game_objects.level_definitions.level1 import definition as level1_def
from src.game_objects.level import Level
from src.game_objects.enemy import Enemy
from src.game_objects.player import Player
from src.game_objects.script import ScriptBuilder
from src.game_objects.route import Route
from src.game_objects.card_type import CardType

from src.render.hand import render_hand
from src.render.script_builder import render_script_builder
from src.render.network import render_network
from src.render.card import CARD_WIDTH, CARD_HEIGHT, generate as gen_card
from src.render.deck_info import render_deck_info
from src.render.end_turn_button import render_end_turn
from src.render.playzone import render_playzone
from src.render.energy_tracker import render_energy_tracker
from src.render.info_section import render_info
from src.render.terminal import render_terminal
from src.render.card_pick import render_card_pick
from src.render.help_text import render_help_text
from src.render.intro_screen import render_intro_screen
from src.render.end_screen import render_end_screen

from src.utils.asset_loader import img_fetch, get_font
from src.utils.router import generate_route
from src.utils.mouse_check import MouseCheck
from src.utils.card_registry import get_new_card, random_card_choices, get_card_stats
from src.utils.action_queue import get_aq

from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, DEVELOPMENT_VERSION
from src.game_state import GameState, get_game_state
from src.starter_deck import add_starter_cards
from src.level_manager import get_level_order


class Game:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock
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
        self.level_order = get_level_order()

        # Initialize arbitrary level and enemy here so rendering doesn't break
        self.level = Level(level1_def)
        self.enemy = Enemy(level1_def)

    def on_enter_state(self, event, state):
        logging.info(f"Entering '{state.id}' state from '{event}' event.")

    def after_setup_level_complete(self):
        self.player.init_round()
        self.script_builder.init_round()
        self.run_action_queue()

    def after_pre_turn_prep_complete(self):
        self.player.start_turn()
        self.player.tags.on_turn_start_player(self.player)
        self.run_action_queue()

    def after_end_turn(self):
        self.player.end_turn()

    def on_enter_run_enemy_script(self):
        for tag in self.enemy.pattern[self.enemy.current_pattern_id].get('self_tags', []):
            self.enemy.tags.add_tag(tag)

    def after_enemy_script_complete(self):
        self.enemy.script = None
        self.enemy_temp_route = None
        self.enemy_route = None
        self.level.remove_depleted_vectors()

    def after_player_script_complete(self):
        self.player.script = None
        self.player_route = None
        for card_id in self.script_builder.clear():
            if self.player.all_cards[card_id].delete_on_execution:
                self.player.deleted_pile.append(card_id)
            else:
                self.player.add_card_to_discard(card_id)
        self.level.remove_depleted_vectors()

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
        logging.info(get_card_stats())

        self.player = Player()
        self.script_builder = ScriptBuilder()
        add_starter_cards(self.player)
        get_game_state().send('loading_complete')

    def level_update(self):
        # Load new level
        if get_game_state().current_state == GameState.setup_level:
            self.level = Level(self.level_order[self.level_ndx])
            self.enemy = Enemy(self.level_order[self.level_ndx])
            self.script_builder.clear()
            self.player.reset()
            get_game_state().send('setup_level_complete')

        elif get_game_state().current_state == GameState.pre_turn_prep:
            self.enemy.next_script()
            self.enemy_temp_route = generate_route(self.level.get_source('ENEMY'), self.enemy.script)
            get_game_state().send('pre_turn_prep_complete')

        elif get_game_state().current_state == GameState.run_enemy_script:
            if not self.enemy_route:
                self.enemy_route = Route(self.level.get_source('ENEMY'), 'ENEMY')
                self.enemy.script.on_node_advance(None, self.enemy_route.node_path[-1], self.player, autoplay_vector=True)
                return
            pygame.time.wait(1500)  # Delay enemy action for clarity

            self.enemy_route.choose_next_node_from_route(self.enemy_temp_route)
            success = self.enemy.script.on_node_advance(self.enemy_route.edge_path[-1], self.enemy_route.node_path[-1], self.player, autoplay_vector=True)
            if not success or self.enemy_route.is_path_complete():
                get_game_state().send('enemy_script_complete')

        elif get_game_state().current_state == GameState.end_of_level:
            # Placeholder state for end of a level
            pygame.time.wait(1500)
            get_game_state().send('end_of_level_progress')

    def check_events(self):
        m_x, m_y = pygame.mouse.get_pos()
        self.mouseover_text = self.mouse_check.on_mouseover_object(m_x, m_y)

        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Window X clicked
                pygame.quit()

            # Debug actions to change player/opponent health
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFTBRACKET:
                self.player.health -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHTBRACKET:
                self.enemy.health -= 1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_check.mouse_down(m_x, m_y)
                if (get_game_state().current_state == GameState.wait_for_player and
                        ((card_ndx := self.mouse_check.has_selected_prefix(m_x, m_y, 'CARD', False)) is not None)):
                    self.player.start_drag(self.player.current_hand[card_ndx])
                    get_game_state().send('start_drag')

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if get_game_state().current_state == GameState.wait_for_player:
                    if self.mouse_check.has_selected(m_x, m_y, 'END_TURN'):
                        self.end_turn()
                    elif self.mouse_check.has_selected(m_x, m_y, 'SEND_SCRIPT'):
                        self.send_script()

                if get_game_state().current_state == GameState.card_drag:
                    card = self.player.get_dragged_card()
                    logging.info(f'No longer dragging "{self.player.dragged}"')
                    get_game_state().send('card_drop')
                    if (script_ndx := self.mouse_check.has_selected_prefix(m_x, m_y, 'SCRIPT', False)) is not None:
                        self.play_card_on_script_builder(script_ndx, card)
                    elif (node_id := self.mouse_check.has_selected_prefix(m_x, m_y, 'NODE', False)) is not None:
                        node = self.level.nodes[node_id]
                        self.play_card_on_node(node, card)
                    elif self.mouse_check.has_selected(m_x, m_y, 'PLAYZONE', False):
                        self.play_generic_card(card)
                    else:
                        self.player.add_card_to_hand(self.player.dragged)  # Card drop in invalid location
                    self.player.dragged = None

                elif get_game_state().current_state == GameState.run_player_script:
                    if (node_id := self.mouse_check.has_selected_prefix(m_x, m_y, 'NODE')) is not None:
                        # Select the next node in the path
                        node = self.level.nodes[node_id]
                        self.node_selected(node)
                    if (vector_ndx := self.mouse_check.has_selected_prefix(m_x, m_y, 'INSTALL_VECTOR')) is not None:
                        installed_vector = self.player.script.vector.pop(vector_ndx)
                        self.player_route.node_path[-1].install_vector(installed_vector)
                        self.player.script.tags.on_vector_install(self.player_route.node_path[-1], installed_vector, self.player.get_player_info_dict())

                elif get_game_state().current_state == GameState.card_pick:
                    if (pick_card_ndx := self.mouse_check.has_selected_prefix(m_x, m_y, 'PICK_CARD')) is not None:
                        self.player.add_card(self.card_choices.pop(pick_card_ndx))
                        # get_game_state().send('end_of_level_progress')  # FIXME: Limit to one card pick
                    elif self.mouse_check.has_selected(m_x, m_y, 'NEXT_BUTTON'):
                        get_game_state().send('end_of_level_progress')

                elif get_game_state().current_state == GameState.intro_screen:
                    if self.mouse_check.has_selected(m_x, m_y, 'START_BUTTON'):
                        get_game_state().send('start_selected')

                elif get_game_state().current_state == GameState.game_end_loss:
                    pass
                elif get_game_state().current_state == GameState.game_end_win:
                    pass

                self.mouse_check.mouse_up()

    def render_screen(self):
        # Clear screen from last frame
        self.screen.fill("black")
        self.screen.blit(self.background, (0, 0))

        self.mouse_check.reset()

        # Render the network
        if get_game_state().current_state == GameState.run_enemy_script:
            render_network(self.screen, self.level, self.player.script, self.enemy.script, [self.enemy_route, self.player_route])
        else:
            interactables, mouseovers = render_network(self.screen, self.level, self.player.script, None, [self.enemy_temp_route, self.player_route])
            self.mouse_check.register_rect(interactables)
            self.mouse_check.register_mouseover_rect(mouseovers)

        # Render info
        mouseovers = render_info(self.screen, self.player)
        self.mouse_check.register_mouseover_rect(mouseovers)
        mouseovers = render_info(self.screen, self.enemy)
        self.mouse_check.register_mouseover_rect(mouseovers)

        # Render terminal
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
        if get_game_state().current_state == GameState.card_pick:
            interactables = render_card_pick(self.screen, self.card_choices)
            self.mouse_check.register_rect(interactables)

        if get_game_state().current_state == GameState.intro_screen:
            interactables = render_intro_screen(self.screen)
            self.mouse_check.register_rect(interactables)

        if get_game_state().current_state == GameState.game_end_loss:
            render_end_screen(self.screen, win=False)
        elif get_game_state().current_state == GameState.game_end_win:
            render_end_screen(self.screen, win=True)

        m_x, m_y = pygame.mouse.get_pos()

        # Render mouseover text
        if self.mouseover_text:
            render_help_text(self.screen, self.mouseover_text, m_x, m_y)

        # Render dragged card to mouse position
        if get_game_state().current_state == GameState.card_drag and self.player.dragged is not None:
            self.screen.blit(
                gen_card(self.player.get_dragged_card()),
                (m_x - CARD_WIDTH//2, m_y - CARD_HEIGHT//2)
            )

        # Render version
        font = pygame.font.Font(get_font('BrassMono', 'regular'), 30)
        text = font.render(DEVELOPMENT_VERSION, True, 'white')
        self.screen.blit(text, (2, 2))

        pygame.display.flip()  # Displays changed on screen
        self.clock.tick(30)  # limits FPS to 30
        return True

    def node_selected(self, node):
        if node not in self.player_route.get_next_node_options():
            logging.warning(f'Selected node "{node.id}" not an option for next node.')
            return

        self.player_route.choose_next_node(node)
        success = self.player.script.on_node_advance(self.player_route.edge_path[-1], self.player_route.node_path[-1], self.enemy)
        self.run_action_queue()

        if not success or self.player_route.is_path_complete():
            get_game_state().send('player_script_complete')

    def send_script(self, ignore_cost=False):
        if not ignore_cost and not self.player.has_energy(1):
            logging.info(f'Not enough energy to execute script.')
            return

        if not ignore_cost:
            self.player.pay_energy(1)
        self.player.script = self.script_builder.build_script(self.player.get_player_info_dict())
        self.run_action_queue()
        self.player.tags.on_script_creation(self.player.script)
        self.run_action_queue()
        self.player_route = Route(self.level.get_source('PLAYER'), 'PLAYER')
        self.player.script.on_node_advance(None, self.player_route.node_path[-1], self.level)
        get_game_state().send('send_script_selected')

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
            self.run_action_queue()
            self.player.post_card_played(self.player.dragged)

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
            self.run_action_queue()
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
            self.run_action_queue()

    def end_turn(self):
        self.player.tags.on_turn_end_player(self.player)
        self.run_action_queue()

        self.enemy.tags.on_turn_end_enemy(self.enemy)
        self.run_action_queue()

        for node in self.level.nodes.values():
            node.tags.on_turn_end_node(node)
            if node.vector:
                node.vector.tags.on_turn_end_vector(node.vector, node)
        self.run_action_queue()

        get_game_state().send('end_turn')

    def run_action_queue(self):
        queue = get_aq()
        action = queue.get_action()
        while action:
            if action[0] == 'add_card':
                new_card = get_new_card(action[1])
                self.player.add_temp_card(new_card, to=action[2])
            elif action[0] == 'draw_cards':
                self.player.draw(action[1])
            elif action[0] == 'delete_cards':
                card_id_to_delete = []
                for i in range(min(action[2], len(self.player.current_hand))):
                    if action[1] == 'RIGHT':
                        card_id_to_delete.append(self.player.current_hand[-1-i])
                    elif action[1] == 'LEFT':
                        card_id_to_delete.append(self.player.current_hand[i])
                    elif action[1] == 'RANDOM':
                        card_id_to_delete.append(random.choice(
                            [c for c in self.player.current_hand if c not in card_id_to_delete]))
                    else:
                        raise ValueError(f'Unknown card delete argument "{action[1]}"')
                for card_id in card_id_to_delete:
                    self.player.current_hand.remove(card_id)
                    self.player.deleted_pile.append(card_id)
            elif action[0] == 'change_player_health':
                self.player.change_health(action[1])
            elif action[0] == 'change_enemy_health':
                self.enemy.change_health(action[1])
            elif action[0] == 'execute_script':
                self.send_script(ignore_cost=True)
            elif action[0] == 'change_energy':
                self.player.energy += action[1]
            elif action[0] == 'add_player_tag':
                self.player.tags.add_tag(action[1](action[2]))
            elif action[0] == 'add_enemy_tag':
                self.enemy.tags.add_tag(action[1](action[2]))
            elif action[0] == 'card_updates_ward':
                for card in self.player.all_cards_temp.values():
                    if card.type == CardType.WARD and card.ward:
                        card.ward += action[1]
            elif action[0] == 'card_updates_power':
                # TODO: Will break if the change is negative
                for card in self.player.all_cards_temp.values():
                    if card.type == CardType.SCRIPT_PAYLOAD and card.power:
                        card.power += action[1]
            elif action[0] == 'add_script_slot':
                self.script_builder.add_slot(action[1], temporary=True)

            # Get next action
            action = queue.get_action()
