NUM_DECK = 6
class Discards:
   '''
   既に使用されたカード群
   '''
   def __init__(self):
      self.cards = []
      # 2~6のカードを-1,7~9を0, 10~のカードを+1とする
      self.high_row = 0

   # 捨てカード群にカードを追加し、ハイローを変化させる 
   def add_card(self, card):
      self.cards.append(card)
      # カードが2~6の場合は-1, 10以上の場合は+1, それ以外は0とする
      if card.point >= 2 and card.point <= 6 :
         self.high_row += 1
      elif card.point == 10:
         self.high_row -= 1

   # 捨てカードのリセット
   def clear_cards(self):
      self.cards.clear()
      self.high_row = 0
      
   # ハイローを残りデッキ数で割って、トゥルーカウントを算出する
   def get_true_count(self):
      # 残りデッキ数
      deck_num = NUM_DECK*52 # 総デッキ数
      tmp = (deck_num - len(self.cards)) / 52
      rest_deck_num = round(tmp, 1)
      return round(self.high_row / rest_deck_num, 1)