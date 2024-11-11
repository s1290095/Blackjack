INITIAL_CHIP = 100000

class Chip:
    def __init__(self):
        self.balance = INITIAL_CHIP
        self.bet = 0
        self.total_bet = 0 # 総BET額
        self.total_refund_bet = 0 # 総払い出し金額

    def bet_chip(self, bet):
        # 賭け金を設定
        self.balance -= bet
        self.bet = bet
        self.total_bet += bet

    def pay_chip_win(self, is_blackjack):
        # 勝利時の支払い
        if is_blackjack:
            refund_bet = self.bet * 2 * 1.5
            print(f"Bet額：{self.bet}, 返還されるBET：{refund_bet}")
            self.balance += refund_bet
            self.total_refund_bet += refund_bet
        else:
            refund_bet = self.bet * 2
            print(f"Bet額：{self.bet}, 返還されるBET：{refund_bet}")
            self.balance += refund_bet
            self.total_refund_bet += refund_bet

    def pay_chip_lose(self):
        # 敗北時、賭け金は減ったまま
        pass

    def pay_chip_push(self):
        # 引き分け時の支払い
        self.balance += self.bet
