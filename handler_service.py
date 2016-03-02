import dispatcher


class HandlerService:
    def __init__(self, handler):
        self.handler = handler

    def summon(self, card):
        self.handler.write_message(
                {"msg_id": dispatcher.MOVE, "card_id": card.id, "move_to": dispatcher.BATTLE_ZONE})

    def add_to_mana(self, card):
        self.handler.write_message(
                {"msg_id": dispatcher.MOVE, "card_id": card.id, "move_to": dispatcher.MANA_ZONE})

    def destroy(self, card):
        self.handler.write_message(
            {"msg_id": dispatcher.MOVE, "card_id": card.id, "move_to": dispatcher.GRAVEYARD})

    def tap(self, card):
        self.handler.write_message(
            {"msg_id": dispatcher.TAP, "card_id": card.id})

    def untap(self, card):
        self.handler.write_message(
            {"msg_id": dispatcher.UNTAP, "card_id": card.id})

    def move_to_shield(self, card):
        self.handler.write_message(
            {"msg_id": dispatcher.MOVE, "card_id": card.id, "move_to": dispatcher.SHIELDS})
