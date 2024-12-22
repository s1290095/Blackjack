from Game import Game  # Gameクラスをインポート
from base_package.Deck import Deck
from GameManager import GameManager
from BS_package.BSPlayer import BSPlayer
from CC_package.CCPlayer import CCPlayer
from RandomPlayer import RandomPlayer
import matplotlib.pyplot as plt

def main():
    game_manager = GameManager()
    N = 30000
    num = input("使用する戦略を選んでください:1 基本戦略, 2 カードカウンティング:")
    print(num)
    label = ""

    if num == '1':
        game = Game(BSPlayer())
        label = "basic_strategy"
    elif num == '2':
        game = Game(CCPlayer())
        label = "card_counting"

    print(label)

    # matplotlib周りの変数
    data = [] # エージェントの総BET額の推移
    player = game.player

    for cnt in range(N):
        game.check_deck()
        game.reset_game()       # いろいろをリセットする
        game.bet(num)              # 賭ける
        game.deal(num)             # カードを配る
        game.mc_player_turn()
        game_manager.print("ランダムプレイヤーのターンです")
        game.random_player_turn()   # ランダムプレイヤーのターン
        game_manager.print("ディーラーのターンです")
        game.dealer_turn()      # ディーラーのターン
        game.judge()            # 勝敗の判定
        game.pay()              # チップの精算
        data.append(player.chip.balance)
        if cnt == N-1:      # ゲームモードを終了状態に設定
            game.game_count = cnt
            break
    
    print("BlackJackを終了します")
    print(f"{game.game_count+1}回ゲームをしました")
    print(f"{label}の総BET数：{player.chip.balance}, ペイアウト率：{player.get_payput_ratio()}, split回数：{player.split_num}")
    print("")

    # 戦略エージェントの総BET数の推移データ
    fig, ax = plt.subplots()
    ax.plot(data, "r--", label=label)
    ax.legend()
    plt.show()

    # 戦略エージェントの勝率の割合
    fig, ax1 = plt.subplots()
    win_rate_labels = ["win", "draw", "lose"]
    colors = ["red", "yellow", "blue"]

    win_rate_size = [player.win_num, player.draw_num, player.lose_num]
    ax1.pie(win_rate_size, labels=win_rate_labels, colors=colors)
    ax1.set_title(label)
    ax1.legend()
    plt.show()

    return game.player.chip, game.game_count

if __name__ == "__main__":
    main()
