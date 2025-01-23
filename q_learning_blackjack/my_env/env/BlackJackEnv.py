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
        self.action_space = gym.spaces.Discrete(5)  # hit, stand, double down, surrender, split

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
        self.bet_range = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
        
        self.done = False

    def reset(self):
        # 状態を初期化し，初期の観測値を返す
        self.done = False
        self.current_bet = 0

        self.game.reset_game()
        self.game.deal()

        observation = self.observe()

        state = observation["state"]
        bet_state = observation["bet"]

        return state, bet_state
    
    def bet(self, bet):
        
        self.current_bet = bet  # 現在のベット額を記録
        self.game.bet(bet)
    
    def new_game(self):
        self.game = Game()

    def step(self, action):
        # action を実行し，結果を返す
        if action == 0:
            action_str = 'st'  # Stand
        elif action == 1:
            action_str = 'h'  # Hit
        elif action == 2:
            action_str = 'dd'  # Double down
        elif action == 3:
            action_str = 'sr'  # Surrender
        elif action == 4:
            action_str = 'sp'  # Split
        else:
            print(action)
            print("未定義のActionです")
            print(self.observe())

        self.game.player_step(action_str)

        if self.game.player.done:
            # プレーヤーのターンが終了したとき
            self.game.random_player_turn()
            self.game.dealer_turn()
            q_reward, bet_reward = self.get_reward()
            self.game.check_deck()
        else:
            # プレーヤーのターンを継続するとき
            q_reward = 0
            bet_reward = 0

        reward = {
            "reward" : q_reward,
            "bet_reward" : bet_reward
        }

        state = self.observe()
        self.done = self.is_done()
        return state, reward, self.done, {}
    
    def split_step(self, action):
        # action を実行し，結果を返す
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

        self.game.player_split_step(action_str)

        if self.game.player.hand.split_done:
            q_reward, bet_reward = self.get_split_reward()
            self.game.check_deck()
        else:
            # プレーヤーのターンを継続するとき
            q_reward = 0
            bet_reward = 0

        reward = {
            "reward" : q_reward,
            "bet_reward" : bet_reward
        }

        state = self.split_observe()
        return state, reward, self.done, {}

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
        self.game.judge()
        return_bet = self.game.pay()
        player = self.game.player

        # 通常の報酬ロジック
        if player.judgement == 1 and player.hand.is_blackjack:
            return 1.5, return_bet
        elif player.hand.is_bust():
            return -1.5, return_bet
        return player.judgement, return_bet
    
    def get_split_reward(self):
        # 報酬を返す
        player = self.game.player
        player.split_judge(self.game.dealer)
        return_bet = player.split_pay_chip()
        
        # 通常の報酬ロジック
        if player.split_judgement == 1 and player.hand.split_hand.is_blackjack:
            return 1.5, return_bet
        elif player.hand.split_hand.is_bust():
            return -1.5, return_bet
        return player.split_judgement, return_bet

    def is_done(self):
        if self.game.player.done:
            return True
        else:
            return False

    def observe(self):
        observation = {
            'player_points': self.game.player.hand.calc_final_point(),
            'dealer_upcard': self.game.dealer.hand.hand[0].get_point(),
            'is_soft_hand': int(self.game.player.hand.is_soft_hand)
        }

        bet_observation = {
            'true_count': self.game.discards.get_true_count(),
            'current_bet': self.current_bet
        }

        state = {
            "state" : observation,
            "bet" : bet_observation
        }

        return state
    
    def split_observe(self):
        # 観測値にベット額を含める
        observation = {
            'player_points': self.game.player.hand.calc_final_point(),
            'dealer_upcard': self.game.dealer.hand.hand[0].get_point(),
            'is_soft_hand': int(self.game.player.hand.is_soft_hand)
        }

        bet_observation = {
            'true_count': self.game.discards.get_true_count(),
            'current_bet': self.current_bet
        }

        state = {
            "state" : observation,
            "bet" : bet_observation
        }

        return state
    
# 環境を登録
gym.envs.registration.register(
    id='BlackJack-v3',
    entry_point='my_env.env.BlackJackEnv:BlackJackEnv',
)