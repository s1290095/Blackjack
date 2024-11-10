from base_package.Card import Card

class BasicStrategy:

  def __init__(self):
    self.cards = [Card(suit, rank) \
            for suit in Card.SUITS \
            for rank in Card.RANKS]
    
  # ブラックジャック基本戦略表の辞書（ペアを省略）
  basic_strategy = {
      # ハードハンド
      "hard": {
        (2, 3, 4, 5, 6, 7, 8):  {1:"h", 2: "h", 3: "h", 4: "h", 5: "h", 6: "h", 7: "h", 8: "h", 9: "h", 10: "h"},
        9:  {1:"h", 2: "h", 3: "dd", 4: "dd", 5: "dd", 6: "dd", 7: "h", 8: "h", 9: "h", 10: "h"},
        10: {1:"h", 2: "dd", 3: "dd", 4: "dd", 5: "dd", 6: "dd", 7: "dd", 8: "dd", 9: "dd", 10: "h"},
        11: {1:"h", 2: "dd", 3: "dd", 4: "dd", 5: "dd", 6: "dd", 7: "dd", 8: "dd", 9: "dd", 10: "dd"},
        12: {1:"h", 2: "h", 3: "h", 4: "st", 5: "st", 6: "st", 7: "h", 8: "h", 9: "h", 10: "h"},
        13: {1:"h", 2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "h", 8: "h", 9: "h", 10: "h"},
        14: {1:"h", 2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "h", 8: "h", 9: "h", 10: "h"},
        15: {1:"h", 2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "h", 8: "h", 9: "h", 10: "sr"},
        16: {1:"sr", 2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "h", 8: "h", 9: "h", 10: "sr"},
        (17, 18, 19, 20, 21): {1:"st", 2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "st", 8: "st", 9: "st", 10: "st"},
    },

    "soft": {
                  12: {1:"h", 2: "h", 3: "h", 4: "h", 5: "dd", 6: "dd", 7: "h", 8: "h", 9: "h", 10: "h"},
            (13, 14): {1:"h", 2: "h", 3: "h", 4: "h", 5: "dd", 6: "dd", 7: "h", 8: "h", 9: "h", 10: "h"},
            (15, 16): {1:"h", 2: "h", 3: "h", 4: "dd", 5: "dd", 6: "dd", 7: "h", 8: "h", 9: "h", 10: "h"},
                  17: {1:"h", 2: "h", 3: "dd", 4: "dd", 5: "dd", 6: "dd", 7: "h", 8: "h", 9: "h", 10: "h"},
                  18: {1:"st", 2: "h", 3: "dd", 4: "dd", 5: "dd", 6: "dd", 7: "st", 8: "st", 9: "h", 10: "h"},
        (19, 20, 21): {1:"st", 2: "st", 3: "st", 4: "st", 5: "st", 6: "st", 7: "st", 8: "st", 9: "st", 10: "st"},
    },

    "pair": {
        2: {2:"sp", 3:"sp", 4:"sp", 5:"sp", 6:"sp", 7:"sp", 8:"sp", 9:"sp", 10:"sp", 1:"sp"},
        4: {2:"h", 3:"h", 4:"sp", 5:"sp", 6:"sp", 7:"sp", 8:"h", 9:"h", 10:"h", 1:"h"},
        6: {2:"h", 3:"h", 4:"sp", 5:"sp", 6:"sp", 7:"sp", 8:"h", 9:"h", 10:"h", 1:"h"},
        8: {2:"h", 3:"h", 4:"h", 5:"h", 6:"h", 7:"h", 8:"h", 9:"h", 10:"h", 1:"h"},
        10: {2:"dd", 3:"dd", 4:"dd", 5:"dd", 6:"dd", 7:"dd", 8:"dd", 9:"dd", 10:"h", 1:"h"},
        12: {2:"h", 3:"sp", 4:"sp", 5:"sp", 6:"sp", 7:"h", 8:"h", 9:"h", 10:"h", 1:"h"},
        14: {2:"sp", 3:"sp", 4:"sp", 5:"sp", 6:"sp", 7:"sp", 8:"h", 9:"h", 10:"h", 1:"h"},
        16: {2:"sp", 3:"sp", 4:"sp", 5:"sp", 6:"sp", 7:"sp", 8:"sp", 9:"sp", 10:"sp", 1:"sp"},
        18: {2:"sp", 3:"sp", 4:"sp", 5:"sp", 6:"sp", 7:"st", 8:"sp", 9:"sp", 10:"st", 1:"st"},
        20: {2:"st", 3:"st", 4:"st", 5:"st", 6:"st", 7:"st", 8:"st", 9:"st", 10:"st", 1:"st"},
    }
  }

# プレイヤーの手札、ディーラーの手札からアクションを決定します
  def get_action(self, is_pair, is_soft, player_hand, dealer_upcard):
    if is_pair:
        return self.basic_strategy["pair"][player_hand][dealer_upcard]
    else:
        if is_soft:
            # softハンドの範囲に基づいてアクションを選択
            if player_hand in self.basic_strategy["soft"]:
                return self.basic_strategy["soft"][player_hand][dealer_upcard]
            elif 13 <= player_hand <= 14:
                return self.basic_strategy["soft"][(13, 14)][dealer_upcard]
            elif 15 <= player_hand <= 16:
                return self.basic_strategy["soft"][(15, 16)][dealer_upcard]
            elif player_hand in (19, 20, 21):
                return self.basic_strategy["soft"][(19, 20, 21)][dealer_upcard]
        else:
            # hardハンドの範囲に基づいてアクションを選択
            if player_hand in self.basic_strategy["hard"]:
                return self.basic_strategy["hard"][player_hand][dealer_upcard]
            elif 2 <= player_hand <= 8:
                return self.basic_strategy["hard"][(2, 3, 4, 5, 6, 7, 8)][dealer_upcard]
            elif player_hand in (17, 18, 19, 20, 21):
                return self.basic_strategy["hard"][(17, 18, 19, 20, 21)][dealer_upcard]

    # 該当するキーがない場合はエラーメッセージ
    raise ValueError(f"不正な手札: player_hand={player_hand}, dealer_upcard={dealer_upcard}")
