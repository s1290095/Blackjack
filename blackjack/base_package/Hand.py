from base_package.SplitHand import SplitHand

class Hand:
    """
    手札クラス
    """
    def __init__(self):
        self.hand = []
        self.split_hand = SplitHand()
        self.is_soft_hand = False
        self.is_pair = False
        self.is_blackjack = False
        self.is_split = False  # splitを行ったかどうか
        self.split_done = False # split行動が終了したか
        self.ace_count = 0
        self.reduce_count = 0

    def add_card(self, card):
        # 手札にカードを加える処理
        if card.rank == 1:
            self.ace_count += 1
        self.hand.append(card)
        self.check_soft_hand()
        self.check_pair_hand()

    def check_soft_hand(self):
        # ソフトハンド（Aを含む手札）かチェックする
        self.sum_point()
        # Aの数が1以上で、Aを11に出来る数が1以上の場合
        self.is_soft_hand = self.ace_count > 0 and self.reduce_count > 0

    def check_blackjack(self):
        if self.sum_point() == 21:
            self.is_blackjack = True

    def sum_point(self):
        # 手札のポイントを計算
        total = sum(card.point for card in self.hand)
        self.reduce_count = 0

        # A を11としてカウントできる限り、合計が21を超えないように調整
        while self.ace_count > 0 and total + 10 <= 21:
            total += 10  # A のうち1つを11としてカウント
            self.reduce_count += 1

        return total

    def calc_final_point(self):
        # Dealerと勝負するときのポイントを計算
        return self.sum_point()

    def is_bust(self):
        # 手札がBUSTかどうか判定
        return self.sum_point() > 21
    
    # 手札がペアハンドか
    def check_pair_hand(self):
        if len(self.hand) != 2 or self.is_split: # 手札が二枚ではない場合
            self.is_pair = False
            return

        card1 = self.hand[0]
        card2 = self.hand[1]
        self.is_pair = card1.rank == card2.rank

    def deal(self, card):
        # Deal時の処理
        self.add_card(card)

    def hit(self, card):
        # Hit時の処理
        self.add_card(card)
