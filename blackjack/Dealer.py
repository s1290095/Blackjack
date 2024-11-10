from base_package.Hand import Hand
from base_package.Chip import Chip

class Dealer:
    def __init__(self):
        self.hand = Hand()
        self.chip = Chip()
        self.message_on = False

    def init_dealer(self):
        # 手札や各フラグを初期化する
        self.hand = Hand()
        self.done = False

    def deal(self, card):
        # 最初に2枚配る処理
        self.hand.add_card(card)

    def hit(self, card):
        # Hit時の処理（カードを引き、バスト判定）
        self.hand.add_card(card)
        if self.hand.is_bust():
            if self.message_on:
                print("バーストしました")
            self.done = True  # バストした場合、ターン終了
