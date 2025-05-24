# Advanced event schema/flat logger, S2.3/S2.4-compliant
import datetime
from collections.abc import Sequence
from typing import Any, Literal

import pandas as pd

EventType = Literal[
    "simulation_start",
    "game_start",
    "turn_start",
    "dice_roll",
    "move_attempt",
    "tiles_flipped",
    "invalid_move",
    "no_valid_moves",
    "turn_end",
    "game_end",
    "simulation_end",
]


class GameEvent(dict[str, Any]):
    """
    Flat structure for game events, matches full project advice.
    See logger-advice.md for expected field keys.
    """

    pass


class InMemoryEventLogger:
    def __init__(self) -> None:
        self.events: list[GameEvent] = []

    def _add_base_context(
        self,
        sim_id: str | int | None,
        game_id: str | int | None,
        player_id: str | None = None,
        turn_idx: int | None = None,
        move_in_turn_idx: int | None = None,
    ) -> dict[str, Any]:
        context = {
            "timestamp": datetime.datetime.now(datetime.UTC),
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

    def log_event(self, event_type: EventType, **kwargs: Any) -> None:
        event = GameEvent({"event_type": event_type, **kwargs})
        if "timestamp" not in event:
            event["timestamp"] = datetime.datetime.now(datetime.UTC)
        self.events.append(event)

    def log_dice_roll(
        self,
        sim_id: str | int | None,
        game_id: str | int | None,
        player_id: str,
        turn_idx: int,
        roll_values: list[int],
        tiles_up: list[int],
    ) -> None:
        evt = {
            **self._add_base_context(sim_id, game_id, player_id, turn_idx),
            "event_type": "dice_roll",
            "dice_roll_values": tuple(roll_values),
            "dice_roll_total": sum(roll_values),
            "tiles_up_before_move": list(tiles_up),
        }
        self.events.append(GameEvent(evt))

    def log_move_attempt(
        self,
        sim_id: str | int | None,
        game_id: str | int | None,
        player_id: str,
        turn_idx: int,
        move_idx: int,
        strategy: str,
        chosen_combo: Sequence[int],
        tiles_up: Sequence[int],
        roll_total: int,
        is_valid: bool,
        tiles_flipped: Sequence[int] | None = None,
        final_tiles_up: Sequence[int] | None = None,
    ) -> None:
        evt = {
            **self._add_base_context(sim_id, game_id, player_id, turn_idx, move_idx),
            "event_type": "move_attempt",
            "strategy_used": strategy,
            "chosen_combo": tuple(chosen_combo) if chosen_combo else None,
            "tiles_up_before_move": list(tiles_up),
            "dice_roll_total": roll_total,
            "is_combo_valid": is_valid,
        }
        if is_valid and tiles_flipped and final_tiles_up is not None:
            evt["event_type"] = "tiles_flipped"
            evt["tiles_flipped"] = tuple(tiles_flipped)
            evt["tiles_up_after_move"] = list(final_tiles_up)
        elif not is_valid and chosen_combo:
            evt["event_type"] = "invalid_move"
        elif not chosen_combo:
            evt["event_type"] = "no_valid_moves"
        self.events.append(GameEvent(evt))

    def log_turn_end(
        self,
        sim_id: str | int | None,
        game_id: str | int | None,
        player_id: str,
        turn_idx: int,
        final_board_state: list[int],
        turn_score: int,
        shut_box: bool,
    ) -> None:
        evt = {
            **self._add_base_context(sim_id, game_id, player_id, turn_idx),
            "event_type": "turn_end",
            "tiles_up_after_move": list(final_board_state),
            "turn_score": turn_score,
            "shut_box_achieved": shut_box,
        }
        self.events.append(GameEvent(evt))

    def log_game_start(
        self,
        sim_id: str | int | None,
        game_id: str | int | None,
        player_ids: list[str],
        num_dice: int,
    ) -> None:
        evt = {
            **self._add_base_context(sim_id, game_id),
            "event_type": "game_start",
            "player_id": ", ".join(player_ids),
            "num_dice_rolled": num_dice,
        }
        self.events.append(GameEvent(evt))

    def log_game_end(
        self,
        sim_id: str | int | None,
        game_id: str | int | None,
        winner_id: str | None,
        player_scores: dict[str, int],
    ) -> None:
        evt = {
            **self._add_base_context(sim_id, game_id),
            "event_type": "game_end",
            "winner_id": winner_id,
            "all_player_scores": player_scores,
        }
        self.events.append(GameEvent(evt))

    def to_df(self) -> pd.DataFrame:
        if not self.events:
            return pd.DataFrame()
        return pd.DataFrame(self.events)

    def clear_events(self) -> None:
        self.events = []
