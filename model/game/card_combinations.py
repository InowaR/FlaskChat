from model.game.player import Player

deck = {
    'spades': ['♠2', '♠3', '♠4', '♠5', '♠6', '♠7', '♠8', '♠9', '♠10', '♠J', '♠Q', '♠K', '♠A'],
    'hearts': ['♥2', '♥3', '♥4', '♥5', '♥6', '♥7', '♥8', '♥9', '♥10', '♥J', '♥Q', '♥K', '♥A'],
    'diamonds': ['♦2', '♦3', '♦4', '♦5', '♦6', '♦7', '♦8', '♦9', '♦10', '♦J', '♦Q', '♦K', '♦A'],
    'clubs': ['♣2', '♣3', '♣4', '♣5', '♣6', '♣7', '♣8', '♣9', '♣10', '♣J', '♣Q', '♣K', '♣A']
}


# player1_hand = ['♠4', '♣K']
# player2_hand = ['♦K', '♥A']
#
# print(deck['spades'])
#
#
def highest_card(dict_players_cards: dict) -> str:
    print(dict_players_cards)
    d = {}
    for p in dict_players_cards.values():
        d[p['name']] = max(p['hand'])
    max_value = None
    max_keys = []
    for key, value in d.items():
        if max_value is None or value > max_value:
            max_value = value
            max_keys = [key]
        elif value == max_value:
            max_keys.append(key)
    if len(max_keys) > 1:
        return 'Ничья'
    else:
        return max_keys[0]


# list_players = []
#
# player1 = Player('Alex')
# player2 = Player('Maria')
#
# player1.hand = ['♠5', '♣2']
# player2.hand = ['♦4', '♥2']
#
# list_players.append(player1)
# list_players.append(player2)
#

def check_combinations(list_p: list[Player]) -> str:
    dict_players_cards = {}
    for player in list_p:
        dict_players_cards[player.name] = {'name': player.name, 'hand': []}
        for card in player.hand:
            if card[1] == 'J':
                dict_players_cards[player.name]['hand'].append(11)
            elif card[1] == 'Q':
                dict_players_cards[player.name]['hand'].append(12)
            elif card[1] == 'K':
                dict_players_cards[player.name]['hand'].append(13)
            elif card[1] == 'A':
                dict_players_cards[player.name]['hand'].append(14)
            else:
                dict_players_cards[player.name]['hand'].append(int(card[1]))

    return highest_card(dict_players_cards)


