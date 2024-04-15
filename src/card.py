class Card:
    """カードを表すクラス。

    このクラスはトランプの一枚のカードをモデル化したもので、スートとランクの情報を持つ。
    カードの比較や表示など、基本的な操作をサポートする。

    Attributes:
        suit (str): カードのスート。
        rank (str): カードのランク。

    Tests:
        [x]: test_card

    """

    VALID_SUITS = ["♤", "♡", "♢", "♧"]
    VALID_RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self, suit, rank):
        """カードを初期化する。

        Args:
            suit (str): カードのスート ("♤", "♡", "♢", "♧")
            rank (str): カードのランク ("2"-"10", "J", "Q", "K", "A")

        Raises:
            ValueError: VALID_RANK、VALID_SUIT以外が渡された時に発生。

        Tests:
            [x]: test_card_initialization

        """
        if suit not in self.VALID_SUITS:
            raise ValueError(f"Invalid suit: {suit}. Valid suits are: {', '.join(self.VALID_SUITS)}")
        if rank not in self.VALID_RANKS:
            raise ValueError(f"Invalid rank: {rank}. Valid ranks are: {', '.join(self.VALID_RANKS)}")

        self.suit = suit
        self.rank = rank

    def __str__(self):
        """カードの文字列表現を返す。

        Returns:
            str: カードのランクとスートを並べた文字列。

        Tests:
            [x]: test_card_str_representation

        """
        return f"{self.rank:>2} {self.suit}"

    def __repr__(self):
        """カードのオブジェクト表現を返す。

        Returns:
            str: カードのオブジェクトを文字列表記。

        Tests:
            [x]: test_card_representation

        """
        return f"Card('{self.suit}', '{self.rank}')"
