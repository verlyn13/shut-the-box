from stbsim import Board, DiceManager, Die, Game, Player


def test_tile_and_board_basic():
    b = Board(max_tile_number=9)
    # Tiles are upright initially
    upright = b.get_upright_tiles()
    assert len(upright) == 9
    for t in upright:
        assert t.is_upright
    # Flip some tiles
    b.flip_tiles([1, 2, 3])
    up = b.get_upright_tiles()
    assert {t.number for t in up} == set(range(4, 10))
    # Reset returns all upright
    b.reset()
    assert len(b.get_upright_tiles()) == 9


def test_die_and_dice_manager_roll(monkeypatch):
    # Monkeypatch random so this is deterministic
    def fake_randint(a, b):
        return a  # Always return lower bound

    monkeypatch.setattr("random.randint", fake_randint)
    d = Die()
    assert d.roll() == 1
    assert d.current_value == 1
    mgr = DiceManager()
    out = mgr.roll()
    assert out in ([1, 1], [1, 1, 1])  # Could be 2 dice (default) or odd impl
    assert sum(out) == mgr.get_sum()


def test_player_update_score_and_repr():
    p = Player("Alice")
    assert p.score == 0
    p.update_score(17)
    assert p.score == 17
    r = repr(p)
    assert "Alice" in r and "score=17" in r


def test_game_can_run_basic(monkeypatch, capsys):
    # Patch dice to be deterministic
    rolls = [[3, 4], [9, 3], [2, 2], [1, 2], [5, 3], [6, 2], [5, 1]]
    roll_calls = iter(rolls * 3)

    def fake_roll(self, board=None):
        return next(roll_calls)

    monkeypatch.setattr(DiceManager, "roll", fake_roll)
    p1, p2 = Player("Alice"), Player("Bob")
    g = Game([p1, p2], tiles=6)
    g.start_game()
    assert g.is_game_over()
    assert all(isinstance(p.score, int) for p in g.players)
    # Confirm output mentions winner
    captured = capsys.readouterr().out
    assert "Winner:" in captured
