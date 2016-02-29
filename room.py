class Room:
    player_one = None
    player_two = None
    current_player = None
    number_of_turns = None

    def get_opponent(self, player):
        if self.player_one == player:
            return self.player_two
        else: return self.player_one
