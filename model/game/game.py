import random


class Game:
    def __init__(self):
        self.game_id = random.randint(1, 10)
        self.list_players = []
        self.deck = []
        self.table_cards = []
        self.table_money = 0

    def blind(self):
        value1 = 100
        value2 = 200
        p1 = self.list_players[0]
        p2 = self.list_players[1]
        p1.money -= value1
        p2.money -= value2
        self.table_money += (value1 + value2)
        return value1, value2

    def press_button(self, player_name, button):
        for player in self.list_players:
            if player.name == player_name:
                if button == 'fold':
                    player.round += 1

    def next_round(self):
        for player in self.list_players:
            print(player.round)

    def show_players(self):
        players = []
        for player in self.list_players:
            players.append(player.info())
        return players

    def show_table_cards(self):
        return self.table_cards

    def add_player(self, player):
        self.list_players.append(player)

    def create_deck(self):
        for suit in ["♠", "♥", "♦", "♣"]:
            for rank in range(2, 11):
                self.deck.append(f"{suit}{rank}")
            for rank in ["J", "Q", "K", "A"]:
                self.deck.append(f"{suit}{rank}")
        random.shuffle(self.deck)

    def deal_cards(self):
        for player in self.list_players:
            player.hand = []
            for _ in range(2):
                player.hand.append(self.deck.pop())

    def flop(self):
        for _ in range(3):
            self.table_cards.append(self.deck.pop())
