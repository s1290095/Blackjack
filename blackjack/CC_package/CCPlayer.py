from base_package.Hand import Hand
from base_package.Chip import Chip
from CC_package.Discards import Discards
from BS_package.BasicStrategy import BasicStrategy
from base_package.BasePlayer import BasePlayer

# カードカウンティング戦略を取るエージェント
class CCPlayer(BasePlayer):
    def __init__(self):
        super().__init__()
        self.discards = Discards()
        self.basic_strategy = BasicStrategy()

    # actionを表す文字列を返す（h, st, dd, sr..など）
    def action(self, dealer_upcard):
        hand = self.hand
        player_hand = hand.sum_point()
        # 既にsplitを行っていたら、splitは行わない
        if hand.split_done:
            return self.basic_strategy.get_action(False, hand.is_soft_hand, player_hand, dealer_upcard)
        else :
            return self.basic_strategy.get_action(hand.is_pair, hand.is_soft_hand, player_hand, dealer_upcard)

    # splitの手札のアクション
    def split_action(self, dealer_upcard):
        hand = self.hand.split_hand
        player_hand = hand.sum_point()
        return self.basic_strategy.get_action(False, hand.is_soft_hand, player_hand, dealer_upcard)

    # 捨てカードのハイローでBET額を決定
    def bet(self):
        bet = self.discards.decide_bet()
        self.chip.bet_chip(bet)

    def deal(self, card):
        # 最初に2枚配る処理
        self.hand.add_card(card)
        self.hand.check_pair_hand()
        self.discards.add_card(card)