import random

from model.game.player import Player


class Game:
    def __init__(self):
        # self.game_id = random.randint(1, 10)
        self.game_id = 1
        self.start_blind = False
        self.start_preflop = False
        self.start_flop = False
        self.start_turn = False
        self.start_river = False
        self.list_players = []
        self.deck = []
        self.table_cards = []
        self.table_money = 0
        self.round = 0

    def check_group_round(self) -> int:
        return self.round

    def press_button(self, player_name: str, button: str, round_number: str) -> None:
        for player in self.list_players:
            if player.name == player_name:
                if button == 'fold':
                    if int(round_number) == 0:
                        self.round += 1
                        player.play_preflop = True
                        print('player preflop = True')
                    if int(round_number) == 1:
                        self.round += 1
                        player.play_flop = True
                        print('player flop = True')
                    if int(round_number) == 2:
                        self.round += 1
                        player.play_turn = True
                        print('player turn = True')
                    if int(round_number) == 3:
                        self.round += 1
                        player.play_river = True
                        print('player river = True')

    def check_player_buttons(self, player_name: str) -> tuple:
        for player in self.list_players:
            if player.name == player_name:
                return player.play_preflop, player.play_flop, player.play_turn, player.play_river

    def show_players(self) -> list:
        players = []
        for player in self.list_players:
            players.append(player.info())
        return players

    def show_table_cards(self) -> list:
        return self.table_cards

    def add_player(self, player: Player) -> None:
        self.list_players.append(player)

    def create_deck(self) -> None:
        for suit in ["♠", "♥", "♦", "♣"]:
            for rank in range(2, 11):
                self.deck.append(f"{suit}{rank}")
            for rank in ["J", "Q", "K", "A"]:
                self.deck.append(f"{suit}{rank}")
        random.shuffle(self.deck)

    def deal_cards(self) -> None:
        for player in self.list_players:
            player.hand = []
            for _ in range(2):
                player.hand.append(self.deck.pop())

    def blind(self) -> tuple:
        blind1 = 100
        blind2 = 200
        if not self.start_blind:
            p1 = self.list_players[0]
            p2 = self.list_players[1]
            p1.money -= blind1
            p2.money -= blind2
            self.table_money += (blind1 + blind2)
            self.start_blind = True
            return blind1, blind2
        return blind1, blind2

    def preflop(self) -> None:
        if not self.start_preflop:
            self.create_deck()
            self.deal_cards()
            self.start_preflop = True

    def flop(self) -> list:
        if not self.start_flop:
            for _ in range(3):
                self.table_cards.append(self.deck.pop())
            self.start_flop = True
            return self.table_cards
        return self.table_cards

    def turn(self) -> list:
        if not self.start_turn:
            for _ in range(1):
                self.table_cards.append(self.deck.pop())
            self.start_turn = True
            return self.table_cards
        return self.table_cards

    def river(self) -> list:
        if not self.start_river:
            for _ in range(1):
                self.table_cards.append(self.deck.pop())
            self.start_river = True
            return self.table_cards
        return self.table_cards
