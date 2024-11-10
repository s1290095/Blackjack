from Game import Game  # Gameクラスをインポート
from base_package.Deck import Deck

def main():
    game = Game()  # Gameクラスのインスタンスを生成
    N = 1000

    for cnt in range(N):
        if len(game.deck.cards) < 16:
            game.deck = Deck()  # デッキ枚数をリセット
            game.cc_player.discards.clear_cards()
        game.reset_game()       # いろいろをリセットする
        game.bet()              # 賭ける
        game.deal()             # カードを配る
        game.player_turn()      # プレイヤーのターン
        game.mc_player_turn(game.bs_player)   # BSプレイヤーのターン
        game.mc_player_turn(game.cc_player)   # CCプレイヤーのターン
        game.dealer_turn()      # ディーラーのターン
        game.judge()            # 勝敗の判定
        game.pay()              # チップの精算
        if cnt == N-1:      # ゲームモードを終了状態に設定
            game.game_count = cnt
            break
    
    game.calcurate_win_rate(N)

    print("BlackJackを終了します")
    print(f"{game.game_count}回ゲームをしました")
    print("")
    print(f"bsplayerの総BET数：{game.bs_player.chip.balance}, bsplayerの勝率：{game.bs_player.win_rate}")
    print("")
    print(f"ccplayerの総BET数：{game.cc_player.chip.balance}, ccplayerの勝率：{game.cc_player.win_rate}")

    return game.player.chip, game.game_count

if __name__ == "__main__":
    main()
