
class Card:
    '''
    カードを生成
    数字: A, 2～10, J, Q, K
    スート：スペード，ハート，ダイヤ，クラブ
    '''
    SUITS = '♠♥♦♣'
    RANKS = range(1, 14)  # 通常のRank
    SYMBOLS = "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"
    POINTS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]  # BlackJack用のポイント

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.index = suit + self.SYMBOLS[rank - self.RANKS[0]]
        self.point = self.POINTS[rank - self.RANKS[0]]

    def __repr__(self):
        return self.index
    
    def get_point(self):
        return self.point
