import logging
from statemachine import StateMachine, State


class GameState(StateMachine):
    loading = State(initial=True)  # Init player, init game objects, load everything
    intro_screen = State()
    setup_level = State()  # Load the level and draw up for player's hand
    pre_turn_prep = State()
    wait_for_player = State()
    card_drag = State()
    run_player_script = State()  # Build, enact, and animate script
    run_enemy_script = State()
    end_of_level = State()
    card_pick = State()
    game_end_win = State()
    game_end_loss = State()
    exit_game = State(final=True)


    loading_complete = loading.to(intro_screen)
    start_selected = intro_screen.to(setup_level)
    setup_level_complete = setup_level.to(pre_turn_prep)
    pre_turn_prep_complete = pre_turn_prep.to(wait_for_player)

    send_script_selected = wait_for_player.to(run_player_script)
    player_script_complete = (
        run_player_script.to(end_of_level, cond='player_won_level') |
        run_player_script.to(game_end_loss, cond='player_lost_level') |
        run_player_script.to(wait_for_player, unless=['player_won_level', 'player_lost_level'])
    )

    start_drag = wait_for_player.to(card_drag)
    card_drop = (
        card_drag.to(end_of_level, cond='player_won_level') |
        card_drag.to(game_end_loss, cond='player_lost_level') |
        card_drag.to(wait_for_player, unless=['player_won_level', 'player_lost_level'])
    )

    end_turn = wait_for_player.to(run_enemy_script)
    enemy_script_complete = (
        run_enemy_script.to(end_of_level, cond='player_won_level') |
        run_enemy_script.to(game_end_loss, cond='player_lost_level') |
        run_enemy_script.to(pre_turn_prep, unless=['player_won_level', 'player_lost_level'])
    )

    end_of_level_progress = (
        end_of_level.to(game_end_win, cond='player_won_game') |
        end_of_level.to(card_pick, unless='player_won_game') |
        card_pick.to(setup_level)
    )

    select_exit_game = (
        game_end_loss.to(exit_game) |
        game_end_win.to(exit_game)
    )


game_state = None

def get_game_state(*args):
    global game_state
    if not game_state:
        game_state = GameState(*args)
    return game_state

def change_state(new_state):
    global game_state
    game_state.send(new_state)

def get_state():
    global game_state
    return game_state.current_state
