from my_env.env.blackjack.base_package.Deck import Deck  # Deckクラスを明示的にインポート
from my_env.env.blackjack.Dealer import Dealer
from my_env.env.blackjack.RandomPlayer import RandomPlayer
from my_env.env.blackjack.GameManager import GameManager
from my_env.env.blackjack.Player import Player

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.random_player1 = RandomPlayer()
        self.random_player2 = RandomPlayer()
        self.dealer = Dealer()
        self.game_manager =GameManager()
        self.judgment = 0  # 1:勝ち，0:引き分け, -1:負け
        self.game_count = 0

    def reset_game(self):
        # Player, Dealerの手札をリセット
        self.player.init_player()
        self.random_player1.init_player()
        self.random_player2.init_player()
        self.dealer.init_dealer()
        self.player.done = False

    def bet(self):
        self.random_player1.bet()
        self.random_player2.bet()
        self.player.bet(bet=100)

    def deal(self, n=2):
        # Player, Dealerにカードを配る
        for _ in range(n):
            self.random_player1.deal(self.deck.draw_card())
            self.random_player2.deal(self.deck.draw_card())
            self.player.deal(self.deck.draw_card())
            self.dealer.deal(self.deck.draw_card())

    # ランダムエージェントのアクション
    def random_player_turn(self):
        # ランダムプレイヤー1のターン
        while not self.random_player1.done:
            action = self.random_player1.action()
            self.player_step(action, self.random_player1)

        # ランダムプレイヤー2のターン
        while not self.random_player2.done:
            action = self.random_player2.action()
            self.player_step(action, self.random_player2)

    def player_step(self, action):
        player = self.player
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
        self.game_manager.print(f"手札: {self.dealer.hand.hand} 合計: {self.dealer.hand.sum_point()}")
        while self.dealer.hand.sum_point() < 17:
            self.dealer.hit(self.deck.draw_card())

    def judge(self):
        # 勝敗の判定
        self.game_manager.print(f"ディーラーの手札: {self.dealer.hand.hand} 合計: {self.dealer.hand.sum_point()}")
        self.player.judge(self.dealer)
        self.random_player1.judge(self.dealer)
        self.random_player2.judge(self.dealer)

    def pay(self):
        # chipの支払い
        self.player.pay_chip()
        self.random_player1.pay_chip()
        self.random_player2.pay_chip()

    def check_deck(self):
        if self.deck.get_num_deck() <= 52:
            self.deck = Deck()