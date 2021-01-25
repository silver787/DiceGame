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