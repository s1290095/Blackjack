class GameManager:
  def __init__(self):
    self.deck_num = 6 # 初期デッキ数
    self.reset_card_number = 52 # デッキをリセットする際のデッキ残り枚数
    self.initial_chip = 100000 # 初期チップ数
    self.message_display_flg = False # メッセージを表示するかどうか Trueなら表示
    self.is_play_human = False # 人がプレイするか、プレイする場合はTrue

  def print(self, str):
    if self.message_display_flg:
      print(str)