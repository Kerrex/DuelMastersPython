import json

import tornado.websocket

import dispatcher
import handler_service
from incorrect_action_error import IncorrectActionError
from player import Player
from player import players
from room import Room

room = Room()


class ServerHandler(tornado.websocket.WebSocketHandler):
    def data_received(self, chunk):
        pass

    def open(self):
        print("Websocket opened")
        new_player = Player(handler_service.HandlerService(self))
        if room.player_one is None:
            room.player_one = new_player
            new_player.room = room
        elif room.player_two is None:
            room.player_two = new_player
            new_player.room = room
            room.current_player = room.player_one
            room.start_game()
        players[self] = new_player

    def on_message(self, message):
        try:
            msg = json.loads(message)
            dispatcher.dispatch_message(self, msg)
        except IncorrectActionError:
            self.write_message({"msg_id": -1})

application = tornado.web.Application([
                (r"/", ServerHandler),
])


if __name__ == "__main__":
        application.listen(12345)
        tornado.ioloop.IOLoop.current().start()
