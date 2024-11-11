import random
import copy
from base_package.Card import Card

class Deck:
    '''
    カードがシャッフルされたデッキ（山札を生成）
    '''
    def __init__(self):
        self.NUM_DECK = 6 # 必要に応じて変える
        self.cards = [Card(suit, rank) \
            for suit in Card.SUITS \
            for rank in Card.RANKS]

        if self.NUM_DECK > 1:
            temp_cards = copy.deepcopy(self.cards)
            for i in range(self.NUM_DECK - 1):
                self.cards.extend(temp_cards)
        random.shuffle(self.cards)

    def draw_card(self):
        if self.cards:  # self.cardsが空でない場合
            return self.cards.pop(0)  # 先頭のカードを引き出して返す
        return None  # カードがない場合、Noneを返す
    
    def get_num_deck(self):
        return self.NUM_DECK