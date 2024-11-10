INITIAL_CHIP = 1000

class Chip:
    def __init__(self):
        self.balance = INITIAL_CHIP
        self.bet = 0

    def bet_chip(self, bet):
        # 賭け金を設定
        print(f"{bet}")
        self.balance -= bet
        self.bet = bet

    def pay_chip_win(self):
        # 勝利時の支払い
        self.balance += self.bet * 2

    def pay_chip_lose(self):
        # 敗北時、賭け金は減ったまま
        pass

    def pay_chip_push(self):
        # 引き分け時の支払い
        self.balance += self.bet
