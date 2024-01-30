class Player:
    def __init__(self, name: str):
        self.name = name
        self.money = 1000
        self.hand = []
        self.play_preflop = False
        self.play_flop = False
        self.play_turn = False
        self.play_river = False

    def info(self) -> tuple:
        return self.name, self.money, self.hand
