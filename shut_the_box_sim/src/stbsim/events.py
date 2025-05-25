from typing import TypedDict


class Event(TypedDict):
    """Schema for shut the box simulation events logged at each move/turn/game.
    Fields:
        - sim_id: Simulation run identifier
        - game_id: Game identifier within a simulation
        - turn_idx: Which turn in this game
        - move_idx: Which move (roll/attempt) inside the turn
        - player_id: Player name/ID
        - roll: Tuple of dice rolled (e.g. (3, 5))
        - combo: Tuple of tile numbers flipped (can be empty if bust)
        - score_before: Player's tile sum before move
        - score_after: Player's tile sum after move
        - valid: Whether this move was valid (True) or a bust
        - timestamp: float UNIX epoch time
        - schema_ver: int version tag for event schema evolution
    """

    sim_id: int
    game_id: int
    turn_idx: int
    move_idx: int
    player_id: str
    roll: tuple[int, ...]
    combo: tuple[int, ...]
    score_before: int
    score_after: int
    valid: bool
    timestamp: float
    schema_ver: int
