from card import Card
import random


class Deck:
    """
    デッキを表すクラス。
    52枚のカードからなる標準的なデッキを持っています。

    Attributes:
    - cards (list): カードのリスト。

    Methods:
    - generate_deck(): 52枚のカードを生成します。
    - shuffle(cards): デッキ内のカードをシャッフルします。
    - draw(): デッキの一番上のカードを引きます。
    """

    def __init__(self):
        """
        デッキを初期化し、52枚のカードを生成します。
        """
        self.cards = self.generate_deck()

    def generate_deck(self):
        """
        52枚のカードを生成します。

        Returns:
        - list: シャッフルされたカードのリスト。
        """
        cards = [Card(suit, rank) for rank in Card.VALID_RANKS for suit in Card.VALID_SUITS]
        random.shuffle(cards)
        return cards

    def shuffle(self, cards=None):
        """
        デッキ内のカードをシャッフルします。

        Parameters:
        - cards (list): カードのリスト

        """
        if cards is None:
            cards = self.cards
        random.shuffle(cards)
        self.cards = cards

    def draw(self):
        """
        デッキの一番上のカードを引きます。

        Returns:
        - Card: 引いたカード
        """
        return self.cards.pop()
