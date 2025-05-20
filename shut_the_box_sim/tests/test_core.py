# Minimal test scaffold
# --- TileRack tests ---
from stbsim.core import TileRack


def test_initial_tiles_default() -> None:
    rack = TileRack()
    assert rack.tiles_up == set(range(1, 10))
    assert not rack.is_shut()


def test_initial_tiles_custom() -> None:
    rack = TileRack({1, 2, 5})
    assert rack.tiles_up == {1, 2, 5}


def test_flip_tiles_removes() -> None:
    rack = TileRack({1, 2, 3})
    rack.flip_tiles((2, 3))
    assert rack.tiles_up == {1}


def test_is_combo_valid_true() -> None:
    rack = TileRack({1, 2, 3, 4})
    assert rack.is_combo_valid((1, 3), 4) is True


def test_is_combo_valid_false_not_available() -> None:
    rack = TileRack({2, 5, 8})
    assert not rack.is_combo_valid((2, 8, 7), 17)


def test_is_combo_valid_false_sum() -> None:
    rack = TileRack({4, 5, 6})
    assert not rack.is_combo_valid((4, 5), 8)  # sum is 9


def test_score_and_shut() -> None:
    rack = TileRack({2, 7})
    assert rack.score() == 9
    assert not rack.is_shut()
    rack.flip_tiles((2, 7))
    assert rack.score() == 0
    assert rack.is_shut()


def test_to_dict_sorted() -> None:
    rack = TileRack({7, 2, 3})
    d = rack.to_dict()
    assert d == {"tiles_up": [2, 3, 7]}
