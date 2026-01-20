import logging
from statemachine import StateMachine, State


class GameState(StateMachine):
    loading = State(initial=True)  # Init player, init game objects, load everything
    setup_level = State()  # Load the level and draw up for player's hand
    plan_enemy_turn = State()
    wait_for_player = State()
    card_drag = State()
    choose_script_path = State()
    run_script = State()   # Build, enact, and animate script
    end_of_level = State()
    enemy_turn = State()
    game_end_win = State()
    game_end_loss = State()
    exit_game = State(final=True)


    loading_complete = loading.to(setup_level)
    setup_level_complete = setup_level.to(plan_enemy_turn)
    plan_enemy_turn_complete = plan_enemy_turn.to(wait_for_player)
    send_script_selected = wait_for_player.to(choose_script_path)
    script_path_complete = choose_script_path.to(run_script)
    run_script_complete = (
        run_script.to(game_end_loss, cond='player_lost') |
        run_script.to(end_of_level, cond='player_won') |
        run_script.to(wait_for_player)
    )
    start_drag = wait_for_player.to(card_drag)
    card_drop = (
        card_drag.to(game_end_loss, cond='player_lost') |
        card_drag.to(end_of_level, cond='player_won') |
        card_drag.to(wait_for_player)
    )
    end_turn = wait_for_player.to(enemy_turn)
    enemy_turn_complete = (
        enemy_turn.to(game_end_loss, cond='player_lost') |
        enemy_turn.to(end_of_level, cond='player_won') |
        enemy_turn.to(wait_for_player)
    )
    next_level = (
        end_of_level.to(game_end_win, cond='player_won_game') |
        end_of_level.to(setup_level)
    )
    ready_for_exit_game = (
        game_end_loss.to(game_end_win) |
        game_end_win.to(exit_game)
    )


    def on_enter_state(self, event, state):
        logging.info(f"Entering '{state.id}' state from '{event}' event.")

    def player_won(self):
        pass

    def player_lost(self):
        pass

    def player_won_game(self):
        pass

    def after_card_drop(self):
        pass

    def after_enemy_turn_complete(self):
        # New hand for player
        pass
