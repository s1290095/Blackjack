from base_package.Hand import Hand
from base_package.Chip import Chip
from BS_package.BasicStrategy import BasicStrategy
from base_package.BasePlayer import BasePlayer

class BSPlayer(BasePlayer):
    def __init__(self):
        super().__init__()
        self.basic_strategy = BasicStrategy()

    # actionを表す文字列を返す（h, st, dd, sr..など）
    def action(self, dealer_upcard):
        hand = self.hand
        player_hand = hand.sum_point()
        if hand.split_done:
            return self.basic_strategy.get_action(False, hand.is_soft_hand, player_hand, dealer_upcard)
        else :
            return self.basic_strategy.get_action(hand.is_pair, hand.is_soft_hand, player_hand, dealer_upcard)
    
    def split_action(self, dealer_upcard):
        hand = self.hand.split_hand
        player_hand = hand.sum_point()
        return self.basic_strategy.get_action(False, hand.is_soft_hand, player_hand, dealer_upcard)