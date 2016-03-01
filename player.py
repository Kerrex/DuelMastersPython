import dispatcher
from incorrect_action_error import IncorrectActionError

players = dict()
MOVE = 0


class Player:
    handler_service = None
    room = None
    cards = list()
    current_mana = 0

    def __init__(self, handler_service):
        self.handler_service = handler_service

    def summon(self, card):
        if self.is_in_hand(card) and self.current_mana >= card.mana:
            card.zone = 'BATTLE_ZONE'
            card.sickness = True
            self.current_mana -= card.mana
            self.send_summon_request(card)

            self.tap_mana(card.mana)
        else:
            raise IncorrectActionError('Incorrect action')

    def add_to_mana(self, card):
        if card in self.cards and card.zone == 'HAND':
            card.zone = 'MANA_ZONE'
            self.send_add_to_mana_request(card)
        else:
            raise IncorrectActionError('Incorrect action')

    def attack(self, attacker_card, target_card):
        if self.is_in_battle_zone()\
                and attacker_card.sickness is False \
                and attacker_card.tapped is False\
                and self.get_opponent().is_in_battle_zone(target_card)\
                and target_card.tapped is True:
            if attacker_card.power > target_card.power:
                self.get_opponent().destroy(target_card)
                self.tap(attacker_card)
            elif attacker_card.power < target_card.power:
                self.destroy(attacker_card)
            else:
                self.get_opponent().destroy(target_card)
                self.destroy(attacker_card)
        else:
            raise IncorrectActionError('Incorrect action')

    def destroy(self, card):
        card.zone = 'GRAVEYARD'
        self.handler_service.destroy(card)
        self.get_opponent().handler_service.destroy(card)

    def set_up_shields(self, card):
        for x in self.cards[:5]:
            x.zone = 'SHIELD'
            self.handler_service.move_to_shield(card)
            self.get_opponent().handler_service.move_to_shield(card)

    def is_in_battle_zone(self, card):
        return card in self.cards and card.zone == 'BATTLE_ZONE'

    def is_in_hand(self, card):
        return card in self.cards and card.zone == 'HAND'

    def get_opponent(self):
        return self.room.get_opponent(self)

    def tap(self, card):
        card.tapped = True
        self.handler_service.tap(card)
        self.get_opponent().handler_service.tap(card)

    def send_summon_request(self, card):
        self.handler_service.summon(card)
        self.get_opponent().handler_service.summon(card)

    def send_add_to_mana_request(self, card):
        self.handler_service.add_to_mana(card)
        self.get_opponent().handler_service.add_to_mana(card)

    def get_card_by_id(self, id):
        for e in self.cards:
            if e.id == id:
                return e

    def tap_mana(self, to_tap):
        mana_list = [c for c in self.cards if c.zone == 'MANA_ZONE' and c.tapped is False]
        for c in mana_list:
            self.tap(c)
            to_tap -= 1