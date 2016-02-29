import player
from incorrect_action_error import IncorrectActionError

#ACTIONS
END_OF_TURN = 0
ATTACK = 1
MOVE = 2
TAP = 3
UNTAP = 4

#ZONES
BATTLE_ZONE = 0
MANA_ZONE = 1
HAND = 2
GRAVEYARD = 3
SHIELDS = 4


def move(player, card, move_to):
    if move_to == BATTLE_ZONE:
        player.summon(card)
    elif move_to == MANA_ZONE:
        player.add_to_mana(card)
    else:
        raise IncorrectActionError('Incorrect action')


def dispatch_message(handler, message):
    if player.players.get(handler) != player.players.get(handler).room.current_player:
        raise IncorrectActionError('NOT THIS PLAYER TURN')
    elif message["msg_id"] == END_OF_TURN:
        player.players.get(handler).end_of_turn()
    elif message["msg_id"] == ATTACK:
        player.players.get(handler).attack(message["card_id"], message["target_id"])
    elif message["msg_id"] == MOVE:
        move(player.players.get(handler), message["card_id"], message["move_to"])
    else:
        raise IncorrectActionError('Incorrect action')

