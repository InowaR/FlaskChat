class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1000
        self.hand = []

    def info(self):
        return self.name, self.money, self.hand
