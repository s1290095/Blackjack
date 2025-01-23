from my_env.env.blackjack.base_package.Deck import Deck  # Deckクラスを明示的にインポート
from my_env.env.blackjack.Dealer import Dealer
from my_env.env.blackjack.RandomPlayer import RandomPlayer
from my_env.env.blackjack.GameManager import GameManager
from my_env.env.blackjack.Player import Player
from my_env.env.blackjack.Discards import Discards

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.random_player1 = RandomPlayer()
        self.random_player2 = RandomPlayer()
        self.dealer = Dealer()
        self.game_manager = GameManager()
        self.discards = Discards()
        self.judgment = 0  # 1:勝ち，0:引き分け, -1:負け
        self.game_count = 0

    def reset_game(self):
        # Player, Dealerの手札をリセット
        self.player.init_player()
        self.random_player1.init_player()
        self.random_player2.init_player()
        self.dealer.init_dealer()
        self.player.done = False

    def bet(self, bet):
        self.random_player1.bet()
        self.random_player2.bet()
        self.player.bet(bet)

    def deal(self, n=2):
        # Player, Dealerにカードを配る
        for i in range(n):
            card1 = self.deck.draw_card()
            card2 = self.deck.draw_card()
            card3 = self.deck.draw_card()
            card4 = self.deck.draw_card()
            self.random_player1.deal(card1)
            self.random_player2.deal(card2)
            self.player.deal(card3)
            self.dealer.deal(card4)

            # ディーラーのアップカードは保存
            if i == 1:
                self.discards.add_card(card4)

    # ランダムエージェントのアクション
    def random_player_turn(self):
        # ランダムプレイヤー1のターン
        while not self.random_player1.done:
            action = self.random_player1.action()
            self.ra_player_step(action, self.random_player1)

        # ランダムプレイヤー2のターン
        while not self.random_player2.done:
            action = self.random_player2.action()
            self.ra_player_step(action, self.random_player2)

    def player_step(self, action):
        player = self.player
        self.step(action, player)

    def ra_player_step(self, action, player):
        self.step(action, player)

    def player_split_step(self, action):
        player = self.player
        # Stand, Hit, Double down, Surrender, splitに応じた処理
        if action == "h":
            card = self.deck.draw_card()
            self.discards.add_card(card)
            player.split_hit(card)
        elif action == "st":
            player.split_stand()
        elif action == "dd":
            card = self.deck.draw_card()
            self.discards.add_card(card)
            player.split_double_down(card)
        elif action == "sr":
            player.split_surrender()

    def step(self, action, player):
        if action == "h":
            card = self.deck.draw_card()
            self.discards.add_card(card)
            player.hit(card)
        elif action == "st":
            player.stand()
        elif action == "dd":
            card = self.deck.draw_card()
            self.discards.add_card(card)
            player.double_down(card)
        elif action == "sr":
            player.surrender()
        elif action == "sp":
            card = self.deck.draw_card()
            split_card = self.deck.draw_card()

            self.discards.add_card(card)
            self.discards.add_card(split_card)

            player.split(card) # splitの手札にカードを追加
            player.hand.add_card(split_card) # 通常の手札にカードを追加

    def dealer_turn(self):
        # Dealerがポイントが17以上になるまでカードを引く
        self.game_manager.print(f"手札: {self.dealer.hand.hand} 合計: {self.dealer.hand.sum_point()}")
        while self.dealer.hand.sum_point() < 17:
            card = self.deck.draw_card()
            self.discards.add_card(card)
            self.dealer.hit(card)

    def judge(self):
        # 勝敗の判定
        self.game_manager.print(f"ディーラーの手札: {self.dealer.hand.hand} 合計: {self.dealer.hand.sum_point()}")
        self.player.judge(self.dealer)
        self.random_player1.judge(self.dealer)
        self.random_player2.judge(self.dealer)

    def pay(self):
        # chipの支払い
        self.random_player1.pay_chip()
        self.random_player2.pay_chip()
        return self.player.pay_chip()

    def check_deck(self):
        if self.deck.get_num_deck() <= 52:
            self.deck = Deck()
            self.discards.clear_cards()