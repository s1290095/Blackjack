class CountingTable:
  # カードカウンティング戦略表の辞書
  # プレイヤーの手札: ディーラーのアップカード: インデックス番号
  illustrious_18 = {
        16: {10: 0},
        15: {10: 4},
        20: {5: 5},
        20: {6: 4},
        10: {10: 4},
        12: {3: 2},
        12: {2: 3},
        11: {1: 1},
        9: {2: 1},
        10: {1: 4},
        9: {7: 3},
        16: {9: 5},
        13: {2: -1},
        12: {4: 0},
        12: {5: -2},
        12: {6: -1},
        13: {3: -2}
    }
  
  Fab4_surrenders = {
    14 : {10: 3},
    15 : {10: 0},
    15 : {9: 2},
    15 : {1: 1}
  }

  def get_action(self, is_pair, player_hand, dealer_upcard, high_row):
    action_str = self.get_illustrious_action(is_pair, player_hand, dealer_upcard, high_row)

    if action_str == "thr":
      return self.get_fab4_surrenders_action(player_hand, dealer_upcard, high_row)
    else:
      return action_str

  def get_illustrious_action(self, is_pair, player_hand, dealer_upcard, high_row):

    if player_hand == 20:
      if is_pair and (dealer_upcard == 5 or 6):
        index_num = self.illustrious_18.get(player_hand, {}).get(dealer_upcard, 999)
        return self.check_action(index_num, high_row)
      return "thr"

    "ネストされた辞書から値を取得し、存在しない場合はデフォルト値を返す"
    index_num = self.illustrious_18.get(player_hand, {}).get(dealer_upcard, 999)

    return self.check_action(index_num, high_row)
  
  def get_fab4_surrenders_action(self, player_hand, dealer_upcard, high_row):
    "ネストされた辞書から値を取得し、存在しない場合はデフォルト値を返す"
    index_num = self.Fab4_surrenders.get(player_hand, {}).get(dealer_upcard, 999)
    if high_row >= index_num:
      print("test")
      return "sr"
    else:
      return "thr"
    
  def check_action(self, index_num, high_row):
    if index_num == 999:
      return "thr"
    elif high_row >= index_num:
      return "st"
    else:
      return "h"