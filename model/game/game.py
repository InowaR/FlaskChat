import random


class Game:
    def __init__(self):
        self.game_id = random.randint(1, 10)
        self.list_players = []
        self.deck = []
        self.table_cards = []
        self.table_money = 0
        self.make_preflop = False
        self.make_flop = False
        self.blind1 = 100
        self.blind2 = 200
        self.round = 0

    def blind(self):
        p1 = self.list_players[0]
        p2 = self.list_players[1]
        p1.money -= self.blind1
        p2.money -= self.blind2
        self.table_money += (self.blind1 + self.blind2)
        return self.blind1, self.blind2

    def press_button(self, player_name, button):
        for player in self.list_players:
            if player.name == player_name:
                if button == 'fold':
                    self.round += 1
                if button == 'check':
                    self.round += 1
                if button == 'raise':
                    player.money -= 100
                    self.table_money += 100

    def check_round(self):
        if self.round % 2 == 0:
            print(f'{self.round} - сумма раундов')
            return True
        else:
            print(f'{self.round} - сумма раундов')
            return False

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

    def preflop(self):
        if not self.make_preflop:
            self.create_deck()
            self.deal_cards()
            blind1, blind2 = self.blind()
            self.make_preflop = True
            return blind1, blind2
        else:
            return self.blind1, self.blind2

    def flop(self) -> list:
        if not self.round == 2:
            return []
        elif not self.make_flop:
            for _ in range(3):
                self.table_cards.append(self.deck.pop())
            self.make_flop = True
            return self.table_cards
        else:
            return self.table_cards

