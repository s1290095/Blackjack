from blackjack.base_package.BasePlayer import BasePlayer

class Player(BasePlayer):

    def bet(self, bet):
        self.chip.bet_chip(bet)

    def hit(self, card):
        # Hit時の処理（カードを引き、バスト判定）
        self.hand.add_card(card)
        if self.hand.is_bust():
            self.done = True  # バストした場合、ターン終了

    def pay_chip(self):
        # Chipの精算
        if self.judgment == 1:
            self.game_manager.print("playerの勝ちです")
            self.chip.pay_chip_win()
        elif self.judgment == -1:
            self.game_manager.print("playerの負けです")
            self.chip.pay_chip_lose()
        else:
            self.game_manager.print("playerの引き分けです")
            self.chip.pay_chip_push()

        self.game_manager.print(f"player現在のチップ：{self.chip.balance}")