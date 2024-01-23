class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1000
        self.hand = []

    def __str__(self):
        return f'{self.name} {self.money} {self.hand}'
