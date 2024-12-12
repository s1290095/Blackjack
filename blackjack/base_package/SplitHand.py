class SplitHand:
    """
    手札クラス
    """
    def __init__(self):
        self.hand = []
        self.is_soft_hand = False
        self.is_pair = False
        self.is_blackjack = False
        self.is_split = False  # splitを行ったかどうか
        self.split_done = False # split行動が終了したか

    def add_card(self, card):
        # 手札にカードを加える処理
        self.hand.append(card)
        self.check_soft_hand()

    def check_soft_hand(self):
        # ソフトハンド（Aを含む手札）かチェックする
        self.is_soft_hand = any(card.rank == 1 for card in self.hand)  # Aが含まれているとソフトハンド

    def check_blackjack(self):
        if self.sum_point() == 21:
            print("ブラックジャックだ！")
            self.is_blackjack = True

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
