class Card:
    """
    カードを表すクラス。
    各カードはスートとランクの組み合わせで表されます。

    Attributes:
    - suit (str): カードのスート。
    - rank (str): カードのランク。
    """

    VALID_SUITS = ["♤", "♡", "♢", "♧"]
    VALID_RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self, suit, rank):
        """
        カードを初期化します。

        Parameters:
        - suit (str): カードのスート ("♤", "♡", "♢", "♧")
        - rank (str): カードのランク ("2"-"10", "J", "Q", "K", "A")
        """
        if suit not in self.VALID_SUITS:
            raise ValueError(f"Invalid suit: {suit}. Valid suits are: {', '.join(self.VALID_SUITS)}")
        if rank not in self.VALID_RANKS:
            raise ValueError(f"Invalid rank: {rank}. Valid ranks are: {', '.join(self.VALID_RANKS)}")

        self.suit = suit
        self.rank = rank

    def __str__(self):
        """
        カードの文字列表現を返します。
        """
        return f"{self.rank:>2} {self.suit}"

    def __repr__(self):
        """
        カードのオブジェクト表現を返します。
        """
        return f"Card('{self.suit}', '{self.rank}')"
