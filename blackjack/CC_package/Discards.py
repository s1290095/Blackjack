from base_package.Deck import Deck
from GameManager import GameManager

class Discards:
   '''
   既に使用されたカード群
   '''
   def __init__(self):
      self.game_manager = GameManager()
      self.cards = []
      # 2~6のカードを-1,7~9を0, 10~のカードを+1とする
      self.high_row = 0

   # 捨てカード群にカードを追加し、ハイローを変化させる 
   def add_card(self, card):
      self.cards.append(card)
      # カードが2~6の場合は+1, 10以上の場合は-1, それ以外は0とする
      if card.point >= 2 and card.point <= 6 :
         self.high_row += 1
      elif card.point == 10 or card.point == 1:
         self.high_row -= 1

   # 捨てカードのリセット
   def clear_cards(self):
      self.cards.clear()
      self.high_row = 0

   #  ハイローの値からBET額を決定する
   def decide_bet(self):
      high_row_index = self.get_high_row_index()
      print(high_row_index)
      if high_row_index <= 2:
         return 100
      elif high_row_index > 2 and high_row_index <= 6:
         return 200
      elif high_row_index > 6 and high_row_index <= 8:
         return 300
      elif high_row_index > 8 and high_row_index <= 10:
         return 400
      else:
         return 500
      
   # ハイローインデックスを算出
   def get_high_row_index(self):
      # 残りデッキ数
      unseen_deck_num = self.game_manager.deck_num*52 - len(self.cards) # 使われてないカード数
      return round(self.high_row / unseen_deck_num, 2) * 100