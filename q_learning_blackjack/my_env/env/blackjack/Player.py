from my_env.env.blackjack.base_package.BasePlayer import BasePlayer

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
        refund_bet = 0
        if self.judgement == 1:
            self.game_manager.print("playerの勝ちです")
            refund_bet = self.chip.pay_chip_win(self.hand.is_blackjack)
        elif self.judgement == -1:
            self.game_manager.print("playerの負けです")
            refund_bet = self.chip.pay_chip_lose()
        else:
            self.game_manager.print("playerの引き分けです")
            refund_bet = self.chip.pay_chip_push()

        self.game_manager.print(f"player現在のチップ：{self.chip.balance}")

        return refund_bet