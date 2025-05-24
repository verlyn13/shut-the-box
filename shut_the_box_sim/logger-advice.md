**1. Logger attached to _every_ game by default, or only when specifically provided?**

* **Recommendation:** Make the logger **optional** in the `Game` class constructor, defaulting to `None` (as suggested: `logger: Optional[InMemoryEventLogger] = None`).
* **Rationale:**
    * This keeps the `Game` class flexible. For simple unit tests of game logic, you might not need or want the overhead of logging.
    * Your `Simulation` class (planned for S2.5: `Simulation` class: `run(n_games, ...)`) will be the natural place to instantiate an `InMemoryEventLogger` and pass it to each `Game` instance it creates. This ensures that when you run simulations (especially via the CLI later), logging is active.
    * This aligns with the MVP goal of optionally saving detailed game event logs (Goal 5 for MVP). The option is at the simulation/CLI level.

**2. (If sim runner exists) pass `sim_id`, `game_id` cleanly, or hardcode to 0 for now?**

* **Recommendation:** Design to **pass `sim_id` and `game_id` cleanly**. Avoid hardcoding.
* **Rationale:**
    * Your Sprint 2.4 goal is "Ensure `sim_id`, `game_id`, etc., are populated."
    * The `Simulation` class (S2.5) is the perfect place to manage these:
        * `sim_id`: Could be a UUID for the entire simulation run (e.g., `python -m stbsim.cli --n-games 1000 ...`).
        * `game_id`: Could be an incrementing integer (1 to N) within that simulation or individual UUIDs per game.
    * The `Game` class constructor should accept `sim_id` and `game_id` from the `Simulation` runner.
    * The `Turn` class/logic will manage `turn_idx`, and move attempts within a turn can have a `move_idx`.

---

Now, let's focus on implementing `stbsim/loggers.py` (S2.3) and integrating it (S2.4).

### Implementing `stbsim/loggers.py`

**A. Define the Event Schema (Flat)**

Your sprint guide S2.3 calls for a "flat event schema." `TypedDict` with `total=False` is a good approach for this, making it easy to convert to Pandas later.

```python
# src/stbsim/loggers.py
import datetime
from typing import TypedDict, List, Tuple, Optional, Literal, Any
import pandas as pd # Add 'pandas' to your pyproject.toml dev-dependencies if not already there for the lib itself for this conversion

# Define your event types
EventType = Literal[
    "simulation_start", # Example, if Simulation class also logs
    "game_start",
    "turn_start",
    "dice_roll",        # Records the outcome of a dice roll
    "move_attempt",     # Records the combo a player chose (or decided not to choose)
    "tiles_flipped",    # Records the actual tiles flipped after a valid move
    "invalid_move",     # If a chosen combo was invalid
    "no_valid_moves",   # If player cannot make any move with current roll
    "turn_end",
    "game_end",
    "simulation_end"  # Example
]

class GameEvent(TypedDict, total=False):
    """
    A flat structure for game events.
    'total=False' means not all keys must be present in every event dict.
    """
    # Core Context (should be in most events)
    event_type: EventType
    timestamp: datetime.datetime
    sim_id: Optional[str]
    game_id: Optional[Any] # Could be int or str
    player_id: Optional[str]
    turn_idx: Optional[int]
    move_in_turn_idx: Optional[int] # Tracks multiple moves/decisions within one roll if applicable

    # Event-Specific Fields
    # --- For Dice Rolls ---
    dice_roll_values: Optional[Tuple[int, ...]]
    dice_roll_total: Optional[int]

    # --- For Moves & Board State ---
    tiles_up_before_move: Optional[List[int]]
    chosen_combo: Optional[Tuple[int, ...]] # The combo selected by strategy
    is_combo_valid: Optional[bool]          # If the chosen_combo is valid for the roll & tiles
    tiles_flipped: Optional[Tuple[int, ...]]# Actual tiles flipped
    tiles_up_after_move: Optional[List[int]]

    # --- For Turn/Game End ---
    turn_score: Optional[int]           # Score/state at end of player's turn on their own board
    game_score_for_player: Optional[int] # Final score for the player in the game
    all_player_scores: Optional[dict[str, int]]
    winner_id: Optional[str]
    shut_box_achieved: Optional[bool]

    # --- Other details ---
    strategy_used: Optional[str]
    message: Optional[str] # For generic messages or errors not fitting structured fields
    num_dice_rolled: Optional[int]
    available_combos: Optional[List[Tuple[int, ...]]] # Potentially large, log with caution
```

**B. Implement `InMemoryEventLogger`**

```python
# src/stbsim/loggers.py (continued)

class InMemoryEventLogger:
    def __init__(self):
        self.events: List[GameEvent] = []

    def _add_base_context(
        self,
        sim_id: Optional[str],
        game_id: Optional[Any],
        player_id: Optional[str] = None,
        turn_idx: Optional[int] = None,
        move_in_turn_idx: Optional[int] = None,
    ) -> dict:
        """Helper to build the common part of an event."""
        context = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc),
            "sim_id": sim_id,
            "game_id": game_id,
        }
        if player_id is not None:
            context["player_id"] = player_id
        if turn_idx is not None:
            context["turn_idx"] = turn_idx
        if move_in_turn_idx is not None:
            context["move_in_turn_idx"] = move_in_turn_idx
        return context

    def log_event(self, event_type: EventType, **kwargs):
        """
        Generic event logger. It's up to the caller to ensure kwargs
        match the expected fields for the event_type based on GameEvent.
        This version directly takes all event fields as kwargs.
        """
        event: GameEvent = {"event_type": event_type, **kwargs}
        if "timestamp" not in event: # Add timestamp if not provided by caller
             event["timestamp"] = datetime.datetime.now(datetime.timezone.utc)
        self.events.append(event)

    # --- OR, more specific logging methods (recommended for consistency) ---

    def log_dice_roll(self, sim_id: Optional[str], game_id: Optional[Any], player_id: str, turn_idx: int,
                        roll_values: Tuple[int, ...], tiles_up: List[int]):
        event_data: GameEvent = {
            **self._add_base_context(sim_id, game_id, player_id, turn_idx), # type: ignore
            "event_type": "dice_roll",
            "dice_roll_values": roll_values,
            "dice_roll_total": sum(roll_values),
            "tiles_up_before_move": list(tiles_up) # Log state when roll happens
        }
        self.events.append(event_data)

    def log_move_attempt(self, sim_id: Optional[str], game_id: Optional[Any], player_id: str, turn_idx: int,
                           move_idx: int, strategy: str, chosen_combo: Optional[Tuple[int, ...]],
                           tiles_up: List[int], roll_total: int, is_valid: bool, tiles_flipped: Optional[Tuple[int,...]]=None,
                           final_tiles_up: Optional[List[int]]=None):
        event_data: GameEvent = {
            **self._add_base_context(sim_id, game_id, player_id, turn_idx, move_idx), # type: ignore
            "event_type": "move_attempt", # Or "tiles_flipped" / "invalid_move"
            "strategy_used": strategy,
            "chosen_combo": chosen_combo,
            "tiles_up_before_move": list(tiles_up),
            "dice_roll_total": roll_total, # Assuming roll already logged, but good context
            "is_combo_valid": is_valid,
        }
        if is_valid and tiles_flipped and final_tiles_up is not None:
            event_data["event_type"] = "tiles_flipped"
            event_data["tiles_flipped"] = tiles_flipped
            event_data["tiles_up_after_move"] = final_tiles_up
        elif not is_valid and chosen_combo: # Attempted an invalid combo
             event_data["event_type"] = "invalid_move"
        elif not chosen_combo: # No combo chosen (e.g. strategy returned None)
            event_data["event_type"] = "no_valid_moves" # Or similar

        self.events.append(event_data)


    def log_turn_end(self, sim_id: Optional[str], game_id: Optional[Any], player_id: str, turn_idx: int,
                       final_board_state: List[int], turn_score: int, shut_box: bool):
        event_data: GameEvent = {
            **self._add_base_context(sim_id, game_id, player_id, turn_idx), # type: ignore
            "event_type": "turn_end",
            "tiles_up_after_move": list(final_board_state), # State at end of this player's turn
            "turn_score": turn_score, # Player's board score
            "shut_box_achieved": shut_box
        }
        self.events.append(event_data)

    def log_game_start(self, sim_id: Optional[str], game_id: Optional[Any], player_ids: List[str], num_dice: int):
        event_data: GameEvent = {
            **self._add_base_context(sim_id, game_id), # type: ignore
            "event_type": "game_start",
            "player_id": ", ".join(player_ids), # Special handling for multiple players
            "num_dice_rolled": num_dice
        }
        self.events.append(event_data)

    def log_game_end(self, sim_id: Optional[str], game_id: Optional[Any],
                       winner_id: Optional[str], player_scores: dict[str, int]):
        event_data: GameEvent = {
            **self._add_base_context(sim_id, game_id), # type: ignore
            "event_type": "game_end",
            "winner_id": winner_id,
            "all_player_scores": player_scores
        }
        self.events.append(event_data)


    def get_events_dataframe(self) -> pd.DataFrame:
        if not self.events:
            return pd.DataFrame()
        return pd.DataFrame(self.events)

    def clear_events(self):
        self.events = []
```

**Notes on Logger Design:**
* Using specific methods like `log_dice_roll`, `log_move_attempt`, etc., is generally better than one generic `log_event` because it enforces a more consistent structure for each event type and makes the calling code in `Game`/`Turn` cleaner.
* The `_add_base_context` helper reduces repetition. The `# type: ignore` is because `TypedDict` and `**unpacking` can be tricky for type checkers to fully resolve with partial overlaps, but it's functionally fine.
* You'll need `pandas` as a dependency (e.g., `rye add pandas`).

---

### Integrating Logging into `Game` and `Turn` (S2.4)

The dev report's "Logger Integration Plan" and "Tasks" are your guide here.

1.  **Modify `Game.__init__`**:
    ```python
    # src/stbsim/game.py (or core.py)
    from .loggers import InMemoryEventLogger # Assuming logger is in .loggers
    from typing import Optional, Any

    class Game:
        def __init__(self, players, dice, rng_seed,
                     sim_id: Optional[str] = None, # Passed by Simulation runner
                     game_id: Optional[Any] = None,  # Passed by Simulation runner
                     logger: Optional[InMemoryEventLogger] = None):
            # ... existing setup ...
            self.sim_id = sim_id
            self.game_id = game_id
            self.logger = logger
            self.turn_idx_counter = 0 # To assign turn_idx

            if self.logger:
                player_ids = [p.name for p in self.players] # Or however you get player IDs
                self.logger.log_game_start(self.sim_id, self.game_id, player_ids, self.dice.n_dice)
    ```

2.  **Modify `Turn.play_turn` (or equivalent logic in `Game`):**
    The `Turn` class (S1.5) is the ideal place if it encapsulates the logic for a single player's sequence of rolls and moves. It would need to accept `logger`, `sim_id`, `game_id`, and its `turn_idx`.

    ```python
    # src/stbsim/core.py (or wherever Turn class is)
    class Turn:
        def __init__(self, player, tile_rack, dice, turn_idx, sim_id, game_id, logger):
            self.player = player
            self.tile_rack = tile_rack # This is the specific player's rack instance
            self.dice = dice
            self.turn_idx = turn_idx
            self.sim_id = sim_id
            self.game_id = game_id
            self.logger = logger
            self.move_in_turn_idx_counter = 0
            # ...

        def play_turn(self):
            # ...
            if self.logger:
                # Log turn_start (if you define such an event)
                # self.logger.log_turn_start(...)
                pass

            while True: # Loop for multiple rolls/moves if player keeps going
                self.move_in_turn_idx_counter += 1
                current_tiles_up = list(self.tile_rack.tiles_up) # Before roll/move
                roll_values = self.dice.roll()
                roll_total = sum(roll_values)

                if self.logger:
                    self.logger.log_dice_roll(self.sim_id, self.game_id, self.player.name, self.turn_idx,
                                              roll_values, current_tiles_up)

                # chosen_combo = self.player.choose_combo(roll_total, self.tile_rack.tiles_up, self.tile_rack) # Strategy might need rack state
                # For S1.4, Player.choose_combo just takes roll_total and tiles_up
                chosen_combo = self.player.strategy_fn(roll_total, self.tile_rack.tiles_up)


                is_valid, tiles_to_flip = self.tile_rack.is_combo_valid_and_tiles(chosen_combo, roll_total) # Assume TileRack has such a method

                if self.logger:
                    tiles_after_flip = None
                    if is_valid and chosen_combo:
                        # Temporarily apply to see effect for logging, or log after actual flip
                        # This depends on whether TileRack.flip_tiles mutates then returns status, or checks then mutates
                        # For simplicity, let's assume we log after the attempt.
                        # If flip_tiles also returns the new state, that's useful.
                        # tiles_after_flip = self.tile_rack.peek_flip(chosen_combo) # If such a method exists
                        pass # We'll log after the actual flip or failure

                if is_valid and chosen_combo:
                    self.tile_rack.flip_tiles(chosen_combo)
                    tiles_after_actual_flip = list(self.tile_rack.tiles_up)
                    if self.logger:
                        self.logger.log_move_attempt(self.sim_id, self.game_id, self.player.name,
                                                     self.turn_idx, self.move_in_turn_idx_counter,
                                                     self.player.strategy_fn.__name__, # Or a more descriptive strategy name
                                                     chosen_combo, current_tiles_up, roll_total, True,
                                                     tiles_flipped=chosen_combo, final_tiles_up=tiles_after_actual_flip)

                    if self.tile_rack.is_shut():
                        # Player shut the box! Turn ends.
                        break
                    # Player made a valid move, continues turn with same dice count (standard rules)
                else:
                    # No valid move chosen, or chosen move was invalid. Turn ends.
                    if self.logger:
                         self.logger.log_move_attempt(self.sim_id, self.game_id, self.player.name,
                                                     self.turn_idx, self.move_in_turn_idx_counter,
                                                     self.player.strategy_fn.__name__,
                                                     chosen_combo, current_tiles_up, roll_total, False)
                    break # End turn

            # End of turn
            final_score_for_turn = self.tile_rack.score()
            shut_this_turn = self.tile_rack.is_shut()
            if self.logger:
                self.logger.log_turn_end(self.sim_id, self.game_id, self.player.name, self.turn_idx,
                                         list(self.tile_rack.tiles_up), final_score_for_turn, shut_this_turn)
            # Return relevant turn summary if needed by Game class
            return final_score_for_turn, shut_this_turn
    ```

3.  **Modify `Game.play_game()` to orchestrate and log game end**:
    ```python
    # src/stbsim/game.py (or core.py)
    class Game:
        # ... __init__ ...

        def play_game(self):
            # ... game loop ...
            for current_player in self.players_in_turn_order:
                self.turn_idx_counter += 1
                # Assuming each player has their own TileRack instance, managed by Game
                player_tile_rack = self.tile_racks[current_player.name]

                # Instantiate Turn or call turn logic
                current_turn = Turn(current_player, player_tile_rack, self.dice,
                                    self.turn_idx_counter, self.sim_id, self.game_id, self.logger)
                player_score_for_turn, shut_box_this_turn = current_turn.play_turn()

                # Update game state, check if game over (e.g., player shut the box)
                self.final_scores[current_player.name] = player_score_for_turn # Store final score for player for *this game*
                if shut_box_this_turn:
                    self.winner = current_player # Or however winner is determined
                    break # Game ends immediately if a player shuts the box

            # After game loop (either someone shut the box, or all players busted)
            if not self.winner: # If no one shut the box, determine winner based on lowest score
                # ... logic to determine winner if not already set ...
                pass

            if self.logger:
                winner_id_to_log = self.winner.name if self.winner else None
                self.logger.log_game_end(self.sim_id, self.game_id, winner_id_to_log, self.final_scores)

            return self.winner, self.final_scores
    ```

---

### Unit Tests and Demo File

* **Logger Unit Tests (for `stbsim/loggers.py`)**:
    * Create an `InMemoryEventLogger`.
    * Call its various `log_...` methods with sample data.
    * Assert that `logger.events` contains the expected number of events and that their structure/data is correct.
    * Call `logger.get_events_dataframe()` and assert the DataFrame has the right columns, number of rows, and some sample data matches.
* **Integration Test / Demo File (as per dev report)**:
    * Create a main script (e.g., `scripts/run_logged_game.py` or a test file in `tests/`).
    * Instantiate `InMemoryEventLogger`.
    * Instantiate `Game` with players, dice, a seed, and pass the logger, `sim_id="sim_0"`, `game_id="game_0"`.
    * Run `game.play_game()`.
    * Print `logger.get_events_dataframe()`.
    * Assert basic things about the logged events:
        * Are there `dice_roll` events?
        * Are there `tiles_flipped` or `invalid_move` events?
        * Is there one `game_end` event?
        * Do context IDs (`sim_id`, `game_id`, `player_id`, `turn_idx`) look reasonable?
