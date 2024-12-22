from my_env.env.blackjack.base_package.Hand import Hand
from my_env.env.blackjack.base_package.Chip import Chip
from my_env.env.blackjack.GameManager import GameManager

class BasePlayer:
    def __init__(self):
        self.hand = Hand()
        self.chip = Chip()
        self.split_chip = Chip()
        self.game_manager = GameManager()
        self.hit_flag = False
        self.done = False  # Playerのターン終了を示すフラグ
        self.is_human = False  # True:人がプレイ，False:プレイしない
        self.is_surrender = False # 降参したか
        self.is_split_surrender = False # 降参したか（split）
        self.judgement = 0     # 1:勝ち，0:引き分け, -1:負け
        self.split_judgement = 0
        self.win_num = 0       # 勝った回数
        self.lose_num = 0      # 負けた回数
        self.draw_num = 0      # 引き分け回数
        self.split_num = 0
        self.message_display_flg = False # メッセージ表示フラグ　True：表示、False：非表示

    def init_player(self):
        # 手札や各フラグを初期化する
        self.hand = Hand()
        self.done = False
        self.is_surrender = False
        self.is_split_surrender = False
        self.hit_flag = False

    def bet(self):
        self.chip.bet_chip(bet=10)

    def deal(self, card):
        # 最初に2枚配る処理
        self.hand.add_card(card)

    def hit(self, card):
      # Hit時の処理（カードを引き、バスト判定）
      self.hit_flag = True
      self.hand.add_card(card)
      self.game_manager.print(f"手札: {self.hand.hand} 合計: {self.hand.sum_point()}")
      if self.hand.is_bust():
          self.done = True  # バストした場合、ターン終了

    def stand(self):
        # Stand時の処理
        self.hand.check_blackjack()
        self.done = True

    def double_down(self, card):
        # Double down時の処理（賭け金2倍でカードを1枚追加して終了）
        self.chip.bet_chip(self.chip.bet * 2)
        self.hit(card)
        self.stand()

    def surrender(self):
        # Surrender時の処理
        self.done = True
        self.chip.bet /= 2  # 賭け金の半分が返却される
        self.is_surrender = True

    def split(self, card):
        self.split_chip.bet_chip(self.chip.bet)
        self.hand.split_hand.add_card(self.hand.hand.pop(-1))
        self.hand.split_hand.add_card(card)
        self.hand.is_split = True
        self.split_num += 1

    def split_hit(self, card):
        # Hit時の処理（カードを引き、バスト判定）
        split_hand = self.hand.split_hand
        split_hand.add_card(card)
        print(f"手札: {split_hand.hand} 合計: {split_hand.sum_point()}")
        if split_hand.is_bust():
            self.hand.split_done = True  # バストした場合、ターン終了

    def split_stand(self):
        self.hand.split_hand.check_blackjack()
        self.hand.split_done = True

    def split_double_down(self, card):
        # Double down時の処理（賭け金2倍でカードを1枚追加して終了）
        self.split_chip.bet_chip(self.split_chip.bet * 2)
        self.split_hit(card)
        self.split_stand()

    def split_surrender(self):
        # Surrender時の処理
        self.hand.split_done = True
        self.split_chip.bet /= 2  # 賭け金の半分の半分が返却される
        self.is_split_surrender = True
    
    def judge(self, dealer):
        if self.hand.is_bust():
            self.lose_num += 1
            self.judgement = -1
        elif dealer.hand.is_bust():
            self.win_num += 1
            self.judgement = 1
        elif self.hand.calc_final_point() > dealer.hand.calc_final_point():
            self.win_num += 1
            self.judgement = 1
        elif self.hand.calc_final_point() < dealer.hand.calc_final_point():
            self.lose_num += 1
            self.judgement = -1
        else:
            self.draw_num += 1
            self.judgement = 0
        if self.is_surrender:
            self.judgement = 0

        if self.hand.is_split:
            self.split_judge(dealer)

    def pay_chip(self):
        # Chipの精算
        if self.judgement == 1:
            self.chip.pay_chip_win(self.hand.is_blackjack)
        elif self.judgement == -1:
            self.chip.pay_chip_lose()
        else:
            self.chip.pay_chip_push()

        if self.hand.is_split:
            self.split_pay_chip()

    def split_judge(self, dealer):
        split_hand = self.hand.split_hand
        if split_hand.is_bust():
            self.lose_num += 1
            self.split_judgement = -1
        elif dealer.hand.is_bust():
            self.win_num += 1
            self.split_judgement = 1
        elif split_hand.calc_final_point() > dealer.hand.calc_final_point():
            self.win_num += 1
            self.split_judgement = 1
        elif split_hand.calc_final_point() < dealer.hand.calc_final_point():
            self.lose_num += 1
            self.split_judgement = -1
        else:
            self.draw_num += 1
            self.split_judgement = 0
        if self.is_surrender:
            self.split_judgement = -0.5

    def split_pay_chip(self):
        # Chipの精算
        if self.split_judgement == 1:
            self.split_chip.pay_chip_win(self.hand.split_hand.is_blackjack)
        elif self.split_judgement == -1:
            self.split_chip.pay_chip_lose()
        else:
            self.split_chip.pay_chip_push()

        # 払い戻し金額/総BET額で算出されるペイアウト率
    def get_payput_ratio(self):
        chip = self.chip
        split_chip = self.split_chip
        print(f"合計BET額:{chip.total_bet}, 返還額:{chip.total_refund_bet}, split回数:{self.split_num}")
        chip.total_refund_bet += split_chip.total_refund_bet
        chip.total_bet += split_chip.total_bet
        print(f"合計BET額:{chip.total_bet}, 返還額:{chip.total_refund_bet}")
        return (chip.total_refund_bet / chip.total_bet) * 100