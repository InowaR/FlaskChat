import random
import asyncio


class Game:
    def __init__(self):
        self.game_id = random.randint(1, 10)
        self.list_players = []
        self.deck = []
        self.table_cards = []

    def find_player(self, player_name):
        for player in self.list_players:
            if player.name == player_name:
                return player

    def show_players(self):
        players = []
        for player in self.list_players:
            players.append(player.info())
        return players

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
        self.table_cards.append(self.deck.pop())
