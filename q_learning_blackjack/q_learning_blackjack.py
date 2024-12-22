import sys
import os
import csv  # CSV出力用
from datetime import datetime

# プロジェクトルートを検索パスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from my_env.env.BlackJackEnv import gym

class Agent():
    def __init__(self, epsilon):
        """
        エージェントの初期化
        :param epsilon: ε-greedyの探索率
        """
        self.Q = {}  # Q値を保存する辞書
        self.epsilon = epsilon  # 探索率
        self.reward_log = []  # 報酬履歴を記録

    def policy(self, state, actions):
        """
        ε-greedyポリシーに基づいて行動を選択
        :param state: 現在の状態
        :param actions: 可能な行動のリスト
        :return: 選択した行動のインデックス
        """
        if np.random.random() < self.epsilon:
            return np.random.randint(len(actions))  # ランダムに選択
        else:
            if state in self.Q and sum(self.Q[state]) != 0:
                return np.argmax(self.Q[state])  # 最大のQ値を持つ行動を選択
            else:
                return np.random.randint(len(actions))  # 状態が未学習の場合ランダム

    def init_log(self):
        """報酬ログを初期化"""
        self.reward_log = []

    def log(self, reward):
        """報酬を記録"""
        self.reward_log.append(reward)

    def show_reward_log(self, interval=100, episode=-1):
        """
        報酬履歴を可視化
        :param interval: 可視化する間隔
        :param episode: 現在のエピソード（指定があればログを出力）
        """
        if episode > 0:
            rewards = self.reward_log[-interval:]
            mean = np.round(np.mean(rewards), 3)
            std = np.round(np.std(rewards), 3)
            print(f"Episode {episode}: average_reward={mean} (+/-{std})")
        else:
            indices = list(range(0, len(self.reward_log), interval))
            means = [np.mean(self.reward_log[i:i + interval]) for i in indices]
            stds = [np.std(self.reward_log[i:i + interval]) for i in indices]
            plt.figure()
            plt.title("reward_history")
            plt.xlabel("episode")
            plt.ylabel("reward")
            plt.fill_between(indices, np.array(means) - np.array(stds), np.array(means) + np.array(stds), alpha=0.2)
            plt.plot(indices, means, label="average_reward")
            plt.legend()
            plt.show()

class QLearningAgent(Agent):
    def __init__(self, epsilon=1):
        """Q学習エージェントの初期化"""
        super().__init__(epsilon)

    def learn(self, env, output_interval, episode_count=1000, gamma=0.9, learning_rate=0.1, render=False, report_interval=500):
        """
        Q学習を実行
        :param env: 強化学習環境
        :param episode_count: エピソード数
        :param gamma: 割引率
        :param learning_rate: 学習率
        :param render: 環境を表示するか
        :param report_interval: 報告間隔
        """
        self.init_log()  # 報酬ログを初期化
        actions = list(range(env.action_space.n))  # 行動数を取得
        self.Q = defaultdict(lambda: [0] * len(actions))  # 未訪問状態のQ値は0で初期化

        for e in range(episode_count):
            if e % output_interval == 0 : # output_interval回ごとにゲームをリセット
                env.new_game()
            state = env.reset()  # 環境をリセット
            done = False
            reward_history = []

            while not done:
                if render:
                    env.render()

                action = self.policy(state, actions)  # 行動を選択
                next_state, reward, done, _ = env.step(action)  # 行動を環境に適用

                # Q値の更新
                gain = reward + gamma * max(self.Q[next_state])
                estimated = self.Q[state][action]
                self.Q[state][action] += learning_rate * (gain - estimated)

                state = next_state  # 状態を更新
                reward_history.append(reward)

            self.log(sum(reward_history))  # エピソードの総報酬を記録
            self.epsilon *= 0.999 # 徐々にイプシロンを0に近づける

            if e % report_interval == 0 and e != 0:
                self.show_reward_log(interval=50, episode=e)

        print(f"ペイアウト率：{env.game.player.get_payput_ratio()}")
        env.close()  # 環境を終了

    def save_q_table_to_csv(self):
        """
        QテーブルをCSVファイルに保存（player_handでソート済み）
        """
        # 現在の日付をファイル名に付与
        currentDate = datetime.now().strftime("%Y%m%d%H%M%S")
        filepath = "table_data/q_table_" + currentDate + ".csv"

        # ソート用リストを作成
        q_table_sorted = []
        for state, actions in self.Q.items():
            for action, q_value in enumerate(actions):
                # 状態をタプルに変換
                if isinstance(state, str):
                    states = tuple(map(int, state.strip("()").split(", ")))
                else:
                    states = state

                # actionを行動の文字列に変換
                if action == 0:
                    action_str = "stand"
                elif action == 1:
                    action_str = "hit"
                elif action == 2:
                    action_str = "double down"
                else:
                    action_str = "surrender"
                # ソート用リストに追加
                q_table_sorted.append((states[0], states[1], states[2], action_str, q_value))

        # player_hand（states[0]）で昇順にソート
        q_table_sorted.sort(key=lambda x: (x[0], x[1]))

        # ソート済みのデータをCSVに保存
        with open(filepath, mode="w", newline="") as file:
            writer = csv.writer(file)
            # ヘッダーの書き込み
            writer.writerow(["player_hand", "dealer_hand", "is_soft_hand", "Action", "Q-Value"])
            for row in q_table_sorted:
                writer.writerow(row)

        print(f"ソート済みQテーブルを {filepath} に保存しました。")

def train():
    """
    ブラックジャック環境でQ学習を実行
    """
    env = gym.make('BlackJack-v3')  # Blackjack環境を作成（カスタム環境を想定）
    agent = QLearningAgent()
    agent.learn(env, output_interval=790000, episode_count=800000, report_interval=1000)
    agent.save_q_table_to_csv()  # 学習後にQテーブルを保存
    agent.show_reward_log(interval=500)

if __name__ == "__main__":
    train()
