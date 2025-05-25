class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0

    def update_score(self, score: int) -> None:
        self.score = score

    def __repr__(self) -> str:
        return f"Player({self.name!r}, score={self.score})"
