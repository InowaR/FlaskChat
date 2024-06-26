from model.game.game import Game
from model.game.player import Player


class Service:
    def __init__(self):
        self.list_players = []
        self.list_games = []
        self.list_playing_games = []
        self.list_old_games = []

    def show_players(self, game_id: str) -> list:
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                return game.show_players()

    def show_table_money(self, game_id: str):
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                return game.show_table_money()

    def check_players(self, player_name: str) -> bool:
        for name in self.list_players:
            if name == player_name:
                return True
        return False

    def check_player_money(self, game_id: str, player_name: str) -> bool:
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                return game.check_player_money(player_name)

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
                game = Game(100, 200)
                game.add_player(player1)
                game.add_player(player2)
                self.list_playing_games.append(game)
                return game.game_id
        else:
            return False

    def find_game_by_id(self, game_id: str) -> bool:
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                return True

    def redirect_to_the_game(self, player_name: str) -> int:
        for game in self.list_playing_games:
            for player in game.list_players:
                if player.name == player_name:
                    return game.game_id

    def check_group_round(self, game_id: str) -> int:
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                return game.check_group_round()

    def press_button(self, game_id: str, player_name: str, button: str, player_round: str) -> None:
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                game.press_button(player_name, button, player_round)

    def check_player_buttons(self, game_id: str, player_name: str) -> tuple:
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                return game.check_player_buttons(player_name)

    def new_deal(self, game_id: str):
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                game.check_winner()
                game.new_deal()

    def blind(self, game_id: str) -> tuple:
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                return game.blind()

    def preflop(self, game_id: str) -> tuple:
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                return game.preflop()

    def flop(self, game_id: str) -> list:
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                return game.flop()

    def turn(self, game_id: str) -> list:
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                return game.turn()

    def river(self, game_id: str) -> list:
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                return game.river()

    def check_end_game(self, game_id: str):
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                return game.check_end_game()

    def get_time_game_start(self, game_id: str):
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                return game.get_time_game_start()

    def set_time_game_start(self, game_id: str):
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                return game.set_time_game_start()

    def time_is_over(self, game_id: str, player_name: str, player_round: str):
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                game.press_button(player_name, 'fold', player_round)

    def delete_game(self, game_id: str) -> None:
        for game in self.list_playing_games:
            if game.game_id == int(game_id):
                print(f'Удалена {game.game_id}')
                self.list_old_games.append(game)

    def save_old_poker_games(self):
        with open('poker_data', 'a') as f:
            for game in self.list_old_games:
                f.write(game)
                self.list_old_games.remove(game)
