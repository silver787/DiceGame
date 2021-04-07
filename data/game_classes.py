class Player:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.score = 0


# class that represents a player - used to store all useful information relating to a player for a game session

class Game:
    def __init__(self):
        self.round = 0
        self.turn = 1


# class that represents a game for "duo game" stores which player's turn it is, and what the round number is


class OnlineGame:
    def __init__(self, game_id):
        self.game_id = game_id
        self.player_turn = 0
        self.round_no = 0
        self.ready = False
        self.player_one_name = 'Waiting...'
        self.player_two_name = 'Waiting...'
        self.player_one_score = 0
        self.player_two_score = 0
        self.player_one_roll_one = 0
        self.player_one_roll_two = 0
        self.player_two_roll_one = 0
        self.player_two_roll_two = 0

# class that stores all relevant information needed for the online game - used by the server to talk to the clients
