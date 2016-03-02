class Room:
    player_one = None
    player_two = None
    current_player = None
    number_of_turns = None

    def get_opponent(self, player):
        if self.player_one == player:
            return self.player_two
        else: return self.player_one

    def start_game(self):
        self.player_one.handler_service.handler.write_message({"message": "player one started game"})
        self.player_two.handler_service.handler.write_message({"message": "player two started game"})
