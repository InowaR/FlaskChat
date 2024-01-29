class Player:
    def __init__(self, name: str):
        self.name = name
        self.money = 1000
        self.hand = []
        self.round = 0

    def info(self) -> tuple:
        return self.name, self.money, self.hand
