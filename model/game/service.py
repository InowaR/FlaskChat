from model.game.game import Game
from model.game.player import Player


class Service:
    def __init__(self):
        self.list_players = []
        self.list_games = []
        self.list_playing_games = []

    def show_players(self, number: str) -> list:
        for game in self.list_playing_games:
            if game.game_id == int(number):
                return game.show_players()

    def check_players(self, player_name) -> bool:
        for name in self.list_players:
            if name == player_name:
                return True
        return False

    def add_new_player(self, player_name: str) -> None:
        self.list_players.append(player_name)

    def add_new_game(self) -> bool:
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
            for _ in self.list_games:
                p1, p2 = _
                player1 = Player(p1)
                player2 = Player(p2)
                game = Game()
                game.add_player(player1)
                game.add_player(player2)
                self.list_playing_games.append(game)
                return game.game_id
        else:
            return False

    def find_game_by_id(self, number: str) -> bool:
        for game in self.list_playing_games:
            if game.game_id == int(number):
                return True

    def check_group_round(self, number: str) -> int:
        for game in self.list_playing_games:
            if game.game_id == int(number):
                return game.check_group_round()

    def press_button(self, number: str, player_name: str, button: str, round_number: str) -> None:
        for game in self.list_playing_games:
            if game.game_id == int(number):
                game.press_button(player_name, button, round_number)

    def check_player_buttons(self, number: str, player_name: str) -> tuple:
        for game in self.list_playing_games:
            if game.game_id == int(number):
                return game.check_player_buttons(player_name)

    def preflop(self, number: str) -> tuple:
        for game in self.list_playing_games:
            if game.game_id == int(number):
                return game.preflop()

    def flop(self, number: str) -> list:
        for game in self.list_playing_games:
            if game.game_id == int(number):
                return game.flop()

    def turn(self, number: str) -> list:
        for game in self.list_playing_games:
            if game.game_id == int(number):
                return game.turn()

    def river(self, number: str) -> list:
        for game in self.list_playing_games:
            if game.game_id == int(number):
                return game.river()
