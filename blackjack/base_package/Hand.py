class Hand:
    """
    手札クラス
    """
    def __init__(self):
        self.hand = []
        self.is_soft_hand = False
        self.is_pair =False

    def add_card(self, card):
        # 手札にカードを加える処理
        self.hand.append(card)
        self.check_soft_hand()
        # self.check_pair_hand()

    def check_soft_hand(self):
        # ソフトハンド（Aを含む手札）かチェックする
        self.is_soft_hand = any(card.rank == 1 for card in self.hand)  # Aが含まれているとソフトハンド

    def sum_point(self):
        # 手札のポイントを計算
        total = sum(card.point for card in self.hand)
        if self.is_soft_hand and total + 10 <= 21:
            return total + 10
        return total

    def calc_final_point(self):
        # Dealerと勝負するときのポイントを計算
        return self.sum_point()

    def is_bust(self):
        # 手札がBUSTかどうか判定
        return self.sum_point() > 21
    
    # 手札がペアハンドか
    def check_pair_hand(self):
        if len(self.hand) != 2:
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