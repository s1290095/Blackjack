from Game import Game  # Gameクラスをインポート
from base_package.Deck import Deck
import matplotlib.pyplot as plt

def main():
    game = Game()  # Gameクラスのインスタンスを生成
    N = 8000
    bs_player = game.bs_player
    cc_player = game.cc_player

    # matplotlib周りの変数
    data_bs = [] # 基本戦略のエージェントの総BET額の推移
    data_cc = [] # カードカウンティングのエージェントの総BET額の推移

    for cnt in range(N):
        if len(game.deck.cards) < 16:
            game.deck = Deck()  # デッキ枚数をリセット
            cc_player.discards.clear_cards()
        game.reset_game()       # いろいろをリセットする
        game.bet()              # 賭ける
        game.deal()             # カードを配る
        game.player_turn()      # プレイヤーのターン
        print("BSプレイヤーのターンです")
        game.mc_player_turn(bs_player)   # BSプレイヤーのターン
        print("CCプレイヤーのターンです")
        game.mc_player_turn(cc_player)   # CCプレイヤーのターン
        print("ディーラーのターンです")
        game.dealer_turn()      # ディーラーのターン
        game.judge()            # 勝敗の判定
        game.pay()              # チップの精算
        data_bs.append(bs_player.chip.balance)
        data_cc.append(cc_player.chip.balance)
        if cnt == N-1:      # ゲームモードを終了状態に設定
            game.game_count = cnt
            break
    
    print("BlackJackを終了します")
    print(f"{game.game_count+1}回ゲームをしました")
    print("")
    print(f"bsplayerの総BET数：{bs_player.chip.balance}, ペイアウト率：{bs_player.get_payput_ratio()}")
    print("")
    print(f"ccplayerの総BET数：{cc_player.chip.balance}, ペイアウト率：{cc_player.get_payput_ratio()}")

    # それぞれの戦略エージェントの総BET数の推移データ
    fig, ax = plt.subplots()
    ax.plot(data_bs, "r--", label="basic_strategy")
    ax.plot(data_cc, "b--", label="card_counting")
    ax.legend()
    plt.show()

    # それぞれの戦略エージェントの勝率の割合
    fig, ax1 = plt.subplots()
    fig, ax2 = plt.subplots()
    win_rate_labels = ["win", "draw", "lose"]
    colors = ["red", "yellow", "blue"]

    win_rate_size_bs = [bs_player.win_num, bs_player.draw_num, bs_player.lose_num]
    ax1.pie(win_rate_size_bs, labels=win_rate_labels, colors=colors)
    ax1.set_title("basic_strategy")
    ax1.legend()

    win_rate_size_cc = [cc_player.win_num, cc_player.draw_num, cc_player.lose_num]
    ax2.pie(win_rate_size_cc, labels=win_rate_labels, colors=colors)
    ax2.set_title("card_counting")
    plt.show()

    return game.player.chip, game.game_count

if __name__ == "__main__":
    main()
