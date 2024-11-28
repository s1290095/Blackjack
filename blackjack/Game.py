from base_package.Deck import Deck  # Deckクラスを明示的にインポート
from Player import Player  # Playerクラスも同様にインポート
from Dealer import Dealer
from BS_package.BSPlayer import BSPlayer
from CC_package.CCPlayer import CCPlayer

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.bs_player = BSPlayer()
        self.cc_player = CCPlayer()
        self.dealer = Dealer()
        self.judgment = 0  # 1:勝ち，0:引き分け, -1:負け
        self.game_count = 0
        self.message_on = False  # コンソールにメッセージ表示制御

    def reset_game(self):
        # リセット前にそれぞれのプレイヤーの持ちカードをDisCardsへ移動
        for card in self.bs_player.hand.hand:
            self.cc_player.discards.add_card(card)

        for card in self.dealer.hand.hand:
            self.cc_player.discards.add_card(card)

        for card in self.bs_player.hand.split_hand.hand:
            self.cc_player.discards.add_card(card)

        for card in self.cc_player.hand.split_hand.hand:
            self.cc_player.discards.add_card(card)
            
        # Player, Dealerの手札をリセット
        self.player.init_player()
        self.bs_player.init_player()
        self.cc_player.init_player()
        self.dealer.init_dealer()
        self.player.done = False

    def bet(self):
        # PlayerがBETする
        # Playerの人間フラグがTRUEの場合
        if self.player.is_human == True:
            self.player.bet()
        self.bs_player.bet()
        print(f"BSプレイヤーのBET額：{self.bs_player.chip.bet}")
        self.cc_player.bet()
        print(f"CCプレイヤーのBET額：{self.cc_player.chip.bet}")

    def deal(self, n=2):
        # Player, Dealerにカードを配る
        for _ in range(n):
            if self.player.is_human == True:
                self.player.deal(self.deck.draw_card())
            self.bs_player.deal(self.deck.draw_card())
            self.cc_player.deal(self.deck.draw_card())
            self.dealer.deal(self.deck.draw_card())

    # 機械エージェントのアクション
    def mc_player_turn(self, player):
        print(f"手札: {player.hand.hand} 合計: {player.hand.sum_point()}")
        while not player.done:
            action = player.action(self.dealer.hand.hand[0].get_point())
            self.player_step(action, player)
            while not player.hand.split_done:
                action = player.split_action(self.dealer.hand.hand[0].get_point())
                self.player_split_step(action, player)

    def player_turn(self):
        # プレイヤーのターン処理
        # プレイヤーの人間フラグがFalseの場合、何もしない
        if self.player.is_human == False:
            return
        
        print(f"ディーラーの手札: {self.dealer.hand.hand[0].get_point()}")
        print(f"あなたの手札: {self.player.hand.hand} 合計: {self.player.hand.sum_point()}")
        while not self.player.done:
            action =  input("次の行動を選択してください (h: ヒット, st: スタンド, dd: ダブルダウン, sr: サレンダー): ").lower()  # 自動か入力で行動決定
            self.player_step(action, self.player)

    def player_step(self, action, player):
        # Stand, Hit, Double down, Surrender, splitに応じた処理
        if action == "h":
            player.hit(self.deck.draw_card())
        elif action == "st":
            player.stand()
        elif action == "dd":
            player.double_down(self.deck.draw_card())
        elif action == "sr":
            player.surrender()
        elif action == "sp":
            player.split(self.deck.draw_card()) # splitの手札にカードを追加
            player.hand.add_card(self.deck.draw_card()) # 通常の手札にカードを追加

    def player_split_step(self, action, player):
        # Stand, Hit, Double down, Surrender, splitに応じた処理
        if action == "h":
            player.split_hit(self.deck.draw_card())
        elif action == "st":
            player.split_stand()
        elif action == "dd":
            player.split_double_down(self.deck.draw_card())
        elif action == "sr":
            player.split_surrender()

    def dealer_turn(self):
        # Dealerがポイントが17以上になるまでカードを引く
        print(f"手札: {self.dealer.hand.hand} 合計: {self.dealer.hand.sum_point()}")
        while self.dealer.hand.sum_point() < 17:
            self.dealer.hit(self.deck.draw_card())

    def judge(self):
        # 勝敗の判定
        if self.message_on:
            print(f"ディーラーの手札: {self.dealer.hand.hand} 合計: {self.dealer.hand.sum_point()}")
        if self.player.is_human == True:
            self.player.judge(self.dealer)
        self.bs_player.judge(self.dealer)
        self.cc_player.judge(self.dealer)

    def pay(self):
        if self.player.is_human == True:
            self.player.pay_chip()
        self.bs_player.pay_chip()
        print(f"BSプレイヤーの現在のチップ数：{self.bs_player.chip.balance}")
        self.cc_player.pay_chip()
        print(f"CCプレイヤーの現在のチップ数：{self.cc_player.chip.balance}")