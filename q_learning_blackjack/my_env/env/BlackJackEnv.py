import gym
import gym.spaces
import numpy as np
from my_env.env.blackjack.Player import Player
from my_env.env.BlackJack import Game

class BlackJackEnv(gym.Env):
    metadata = {'render.mode': ['human', 'ansi']}

    def __init__(self):
        super().__init__()

        self.game = Game()

        # action_space, observation_space, reward_range を設定する
        self.action_space = gym.spaces.Discrete(4)  # hit, stand, double down, surrender

        high = np.array([
            30,  # player max
            11,  # dealer max
            1,   # is_soft_hand
        ])
        low = np.array([
            2,  # player min
            1,  # dealer min
            0,  # is_soft_hand false
        ])
        self.observation_space = gym.spaces.Box(low=low, high=high)
        self.reward_range = [-10000, 10000]  # 報酬の最小値と最大値のリスト

        self.done = False
        self.reset()

    def reset(self):
        # 状態を初期化し，初期の観測値を返す
        # 諸々の変数を初期化する
        self.done = False

        self.game.reset_game()
        self.game.bet()
        # self.game.player.chip.balance = 1000  # 学習中は所持金がゼロになることはないとする
        self.game.deal()
        # self.bet_done = True

        return self.observe()
    
    def new_game(self):
        self.game = Game()

    def step(self, action):
        # action を実行し，結果を返す
        # 1ステップ進める処理を記述．戻り値はobservation, reward, done（ゲーム終了したか）, info(追加の情報の辞書)

        if action == 0:
            action_str = 'st'  # Stand
        elif action == 1:
            action_str = 'h'  # Hit
        elif action == 2:
            action_str = 'dd'  # Double down
        elif action == 3:
            action_str = 'sr'  # Surrender
        else:
            print(action)
            print("未定義のActionです")
            print(self.observe())

        self.game.player_step(action=action_str)

        if self.game.player.done:
            # プレーヤーのターンが終了したとき
            self.game.dealer_turn()
            self.game.judge()
            reward = self.get_reward()
            self.game.check_deck()

        else:
            # プレーヤーのターンを継続するとき
            reward = 0

        observation = self.observe()
        self.done = self.is_done()
        return observation, reward, self.done, {}

    def render(self, mode='human', close=False):
        # 環境を可視化する
        # human の場合はコンソールに出力．ansi の場合は StringIO を返す
        pass

    def close(self):
        # 環境を閉じて，後処理をする
        pass

    def seed(self, seed=None):
        # ランダムシードを固定する
        pass

    def get_reward(self):
        # 報酬を返す
        self.game.pay()
        player = self.game.player
        # 勝ちかつブラックジャックの場合、1.5を返す
        if player.judgement == 1 and player.hand.is_blackjack:
            return 1.5
        return player.judgement

    def is_done(self):
        if self.game.player.done:
            return True
        else:
            return False

    def observe(self):
        observation = tuple([
            self.game.player.hand.calc_final_point(),
            self.game.dealer.hand.hand[0].get_point(),  # Dealerのアップカードのみ
            int(self.game.player.hand.is_soft_hand)])

        return observation
    
# 環境を登録
gym.envs.registration.register(
    id='BlackJack-v3',
    entry_point='my_env.env.BlackJackEnv:BlackJackEnv',
)