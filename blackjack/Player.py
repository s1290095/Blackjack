from base_package.Hand import Hand
from base_package.Chip import Chip
from base_package.BasePlayer import BasePlayer

class Player(BasePlayer):

    def bet(self):
        print(f"所持BET額: {self.chip.balance}")
        while 1:
            bet = int(input("betする金額を提示してください: "))
            if bet > self.chip.balance: # 提示BET額が所持BET額より大きい場合
                print("提示BET額が所持BET額を上回っています、再度BETしてください")
                continue
            self.chip.bet_chip(bet)
            break

    def hit(self, card):
        # Hit時の処理（カードを引き、バスト判定）
        self.hand.add_card(card)
        print(f"あなたの手札: {self.hand.hand} 合計: {self.hand.sum_point()}")
        if self.hand.is_bust():
            print("バーストしました")
            self.done = True  # バストした場合、ターン終了

    def pay_chip(self):
        # Chipの精算
        if self.judgment == 1:
            print("playerの勝ちです")
            self.chip.pay_chip_win()
        elif self.judgment == -1:
            print("playerの負けです")
            self.chip.pay_chip_lose()
        else:
            print("playerの引き分けです")
            self.chip.pay_chip_push()

        print(f"player現在のチップ：{self.chip.balance}")