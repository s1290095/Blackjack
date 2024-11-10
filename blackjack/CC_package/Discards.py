from base_package.Deck import Deck
NUM_DECK = 6

class Discards:
    '''
    既に使用されたカード群
    '''
    def __init__(self):
        self.cards = []
        # 2~6のカードを-1,7~9を0, 10~のカードを+1とする
        self.high_row = 4 - (4*NUM_DECK) 

    # 捨てカード群にカードを追加し、ハイローを変化させる 
    def add_card(self, card):
       self.cards.append(card)
       # カードが2~6の場合は-1, 10以上の場合は+1, それ以外は0とする
       if card.point >= 2 and card.point <= 6 :
          self.high_row -= 1
       elif card.point == 10:
          self.high_row += 1

    # 捨てカードのリセット
    def clear_cards(self):
      self.cards.clear()
      self.high_row = 4 - (4*NUM_DECK)

   #  ハイローの値からBET額を決定する
    def decide_bet(self):
       if self.high_row <= -20 :
          return 5
       elif self.high_row <= -5 and self.high_row >= -19:
          return 10
       elif self.high_row == -4:
          return 50
       elif self.high_row == -3:
          return 150
       elif self.high_row == -2:
          return 250
       elif self.high_row >= -1:
          return 300