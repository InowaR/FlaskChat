import random

from model.game.player import Player


class Game:
    def __init__(self):
        self.game_id = random.randint(1, 10)
        self.list_players = []
        self.deck = []
        self.table_cards = []
        self.table_money = 0
        self.blind1 = 100
        self.blind2 = 200
        self.play_preflop = False
        self.play_flop = False
        self.play_turn = False
        self.play_river = False
        self.round = 0

    def blind(self) -> tuple:
        p1 = self.list_players[0]
        p2 = self.list_players[1]
        p1.money -= self.blind1
        p2.money -= self.blind2
        self.table_money += (self.blind1 + self.blind2)
        return self.blind1, self.blind2

    def press_button(self, player_name: str, button: str):
        for player in self.list_players:
            if player.name == player_name:
                if button == 'fold':
                    self.round += 1
                    player.round += 1
                if button == 'check':
                    self.round += 1
                    player.round += 1
                if button == 'raise':
                    player.money -= 100
                    self.table_money += 100

    def group_round_number(self) -> int:
        return self.round

    def player_round_number(self, player_name: str) -> int:
        for player in self.list_players:
            if player.name == player_name:
                return player.round

    def reset_player_round_number(self, player_name: str):
        for player in self.list_players:
            if player.name == player_name:
                player.round = 0

    def show_players(self) -> list:
        players = []
        for player in self.list_players:
            players.append(player.info())
        return players

    def show_table_cards(self) -> list:
        return self.table_cards

    def add_player(self, player: Player):
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

    def preflop(self) -> tuple:
        if not self.play_preflop:
            self.create_deck()
            self.deal_cards()
            blind1, blind2 = self.blind()
            self.play_preflop = True
            return blind1, blind2
        return self.blind1, self.blind2

    def flop(self) -> list:
        if not self.play_flop:
            for _ in range(3):
                self.table_cards.append(self.deck.pop())
            self.play_flop = True
            return self.table_cards
        return self.table_cards

    def turn(self) -> list:
        if not self.play_turn:
            for _ in range(1):
                self.table_cards.append(self.deck.pop())
            self.play_turn = True
            return self.table_cards
        return self.table_cards

    def river(self) -> list:
        if not self.play_river:
            for _ in range(1):
                self.table_cards.append(self.deck.pop())
            self.play_river = True
            return self.table_cards
        return self.table_cards
