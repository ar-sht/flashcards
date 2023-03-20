from fuzzywuzzy import fuzz


class CardSet:
    def __init__(self, cards=None):
        self.cards = cards or {}

    def check_answer(self, question, answer, precision):
        return fuzz.ratio(answer, self.cards[question]) >= precision

    def add_card(self, question, answer):
        self.cards[question] = answer

    def remove_card(self, index):
        del self.cards[list(self.cards.keys())[index]]

    def get(self):
        return self.cards
