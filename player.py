import dispatcher
from incorrect_action_error import IncorrectActionError

players = dict()
MOVE = 0


class Player:
    handler_service = None
    room = None
    cards = list()

    def __init__(self, handler_service):
        self.handler_service = handler_service

    def summon(self, card):
        if card in self.cards and card.zone == 'HAND':
            card.zone = 'BATTLE_ZONE'
            self.handler_service.summon(card)
            card.sickness = True
            # DOPISAĆ TAPOWANIE MANY, PROPONUJĘ LIST COMPREHENSION
        else:
            raise IncorrectActionError('Incorrect action')

    def add_to_mana(self, card):
        if card in self.cards and card.zone == 'HAND':
            card.zone = 'MANA_ZONE'
            self.handler_service.add_to_mana(card)
        else:
            raise IncorrectActionError('Incorrect action')

    def attack(self, attacker_card, target_card):
        if attacker_card in self.cards and attacker_card.zone == 'BATTLE_ZONE' and attacker_card.sickness is False \
                and attacker_card.tapped is False and target_card in self.room.get_opponent(self).cards and \
                        target_card == 'BATTLE_ZONE' and target_card.tapped is True:
            if attacker_card.power > target_card.power:
                self.room.get_opponent(self).destroy(target_card)
                attacker_card.tapped = True
                self.handler_service.tap(attacker_card)
            elif attacker_card.power < target_card.power:
                self.destroy(attacker_card)
            else:
                self.room.get_opponent(self).destroy(target_card)
                self.destroy(attacker_card)

    def destroy(self, card):
        card.zone = 'GRAVEYARD'
        self.handler_service.destroy(card)

    def set_up_shields(self, card):
        for x in self.cards[:5]:
            x.zone = 'SHIELD'
            self.handler_service.move_to_shield(card)

