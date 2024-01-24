from model.game.game import Game
from model.game.player import Player


class Service:
    def __init__(self):
        self.list_players = []
        self.list_games = []
        self.list_playing_games = []

    def check_players(self, player_name):
        for name in self.list_players:
            if name == player_name:
                return True

    def add_new_player(self, player_name):
        self.list_players.append(player_name)

    def add_new_game(self):
        if len(self.list_players) < 2:
            return False
        else:
            for i in range(0, len(self.list_players) - 1, 2):
                self.list_games.append((self.list_players[i], self.list_players[i + 1]))

            if len(self.list_players) % 2 == 1:
                self.list_players = self.list_players[-1:]
            else:
                self.list_players = []
            return True

    def add_new_playing_game(self):
        if self.add_new_game():
            print('Игра началась')
            for _ in self.list_games:
                p1, p2 = _
                player1 = Player(p1)
                player2 = Player(p2)
                game = Game()
                game.add_player(player1)
                game.add_player(player2)
                self.list_playing_games.append(game)
                game.create_deck()
                game.deal_cards()
                return game.game_id
        else:
            print('Ожидайте')
            return False

    def find_game_by_id(self, number: str):
        for game in self.list_playing_games:
            if game.game_id == int(number):
                return game

    def start_game(self, number: str):
        for game in self.list_playing_games:
            if game.game_id == int(number):
                game.create_deck()
                game.deal_cards()
