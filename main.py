import json

import tornado.websocket

import dispatcher
import handler_service
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
        players[self] = new_player

    def on_message(self, message):
        msg = json.loads(message)
        dispatcher.dispatch_message(self, msg)
