import datetime
import random

from model.game.card_combinations import check_combinations
from model.game.player import Player


class Game:
    def __init__(self, blind1: int, blind2: int):
        # self.game_id = random.randint(1, 10)
        self.game_id = 1
        self.time_start = datetime.datetime.now()
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
        self.blind1 = blind1
        self.blind2 = blind2
        self.end_game = False

    def get_time_game_start(self):
        return self.time_start

    def check_group_round(self) -> int:
        return self.round

    def check_player_money(self, player_name: str) -> bool:
        for player in self.list_players:
            if player.name == player_name:
                print(f'Игрок {player.name} - Деньги {player.money}')
                if player.money < 300:
                    return True
                else:
                    return False

    def press_button(self, player_name: str, button: str, player_round: str) -> None:
        for player in self.list_players:
            if player.name == player_name:
                if self.check_player_money(player_name):
                    self.end_game = True
                elif button == 'fold':
                    self.drop_cards(player_name)
                    self.new_deal()
                elif button == 'check':
                    if player_round == '0':
                        self.round += 1
                        player.play_preflop = True
                    elif player_round == '1':
                        self.round += 1
                        player.play_flop = True
                    elif player_round == '2':
                        self.round += 1
                        player.play_turn = True
                    elif player_round == '3':
                        self.round += 1
                        player.play_river = True
                elif button == 'raise':
                    if player_round == '0':
                        self.round += 1
                        player.money -= 300
                        self.table_money += 300
                        player.play_preflop = True
                    elif player_round == '1':
                        self.round += 1
                        player.money -= 300
                        self.table_money += 300
                        player.play_flop = True
                    elif player_round == '2':
                        self.round += 1
                        player.money -= 300
                        self.table_money += 300
                        player.play_turn = True
                    elif player_round == '3':
                        self.round += 1
                        player.money -= 300
                        self.table_money += 300
                        player.play_river = True

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

    def show_table_money(self) -> int:
        return self.table_money

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

    def check_winner(self):
        winner = check_combinations(self.list_players)
        for player in self.list_players:
            if player.name == winner:
                player.money += self.table_money
                self.table_money = 0

    def drop_cards(self, player_name: str):
        for player in self.list_players:
            if player.name != player_name:
                player.money += self.table_money
                self.table_money = 0

    def blind(self) -> tuple:
        if not self.start_blind:
            p1 = self.list_players[0]
            p2 = self.list_players[1]
            p1.money -= self.blind1
            p2.money -= self.blind2
            self.table_money += (self.blind1 + self.blind2)
            self.start_blind = True
            return self.blind1, self.blind2
        return self.blind1, self.blind2

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

    def new_deal(self):
        self.start_blind = False
        self.start_preflop = False
        self.start_flop = False
        self.start_turn = False
        self.start_river = False
        self.deck = []
        self.table_cards = []
        self.table_money = 0
        self.round = 0
        for player in self.list_players:
            player.hand = []
            player.play_preflop = False
            player.play_flop = False
            player.play_turn = False
            player.play_river = False

    def check_end_game(self):
        return self.end_game
