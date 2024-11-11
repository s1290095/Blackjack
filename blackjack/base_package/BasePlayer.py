from base_package.Hand import Hand
from base_package.Chip import Chip

class BasePlayer:
  def __init__(self):
      self.hand = Hand()
      self.chip = Chip()
      self.done = False  # Playerのターン終了を示すフラグ
      self.hit_flag = False  # Player が Hit を選択済みかどうか示すフラグ
      self.is_human = False  # True:人がプレイ，False:プレイしない
      self.judgement = 0     # 1:勝ち，0:引き分け, -1:負け
      self.win_num = 0       # 勝った回数
      self.lose_num = 0      # 負けた回数
      self.draw_num = 0      # 引き分け回数
      self.message_display_flg = False # メッセージ表示フラグ　True：表示、False：非表示

  def init_player(self):
      # 手札や各フラグを初期化する
      self.hand = Hand()
      self.done = False
      self.hit_flag = False

  def bet(self):
    self.chip.bet_chip(bet=10)

  def deal(self, card):
      # 最初に2枚配る処理
      self.hand.add_card(card)

  def hit(self, card):
      # Hit時の処理（カードを引き、バスト判定）
      self.hand.add_card(card)
      self.hit_flag = True
      print(f"手札: {self.hand.hand} 合計: {self.hand.sum_point()}")
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

  def judge(self, dealer):
      if self.hand.is_bust():
          self.lose_num += 1
          self.judgment = -1
      elif dealer.hand.is_bust():
          self.win_num += 1
          self.judgment = 1
      elif self.hand.calc_final_point() > dealer.hand.calc_final_point():
          self.win_num += 1
          self.judgment = 1
      elif self.hand.calc_final_point() < dealer.hand.calc_final_point():
          self.lose_num += 1
          self.judgment = -1
      else:
          self.draw_num += 1
          self.judgment = 0

  def pay_chip(self):
      # Chipの精算
      if self.judgment == 1:
          self.chip.pay_chip_win(self.hand.is_blackjack)
      elif self.judgment == -1:
          self.chip.pay_chip_lose()
      else:
          self.chip.pay_chip_push()

    # 払い戻し金額/総BET額で算出されるペイアウト率
  def get_payput_ratio(self):
      return (self.chip.total_refund_bet / self.chip.total_bet) * 100