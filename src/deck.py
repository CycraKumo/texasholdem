from card import Card
import random


class Deck:
    """デッキを表すクラス。

    52枚のカードからなる標準的なデッキを持つ。

    Attributes:
        cards (list[Card]): カードのリスト。

    Tests:
        [ ]: test_deck

    """

    def __init__(self):
        """デッキを初期化し、52枚のカードを生成する。

        """
        self.cards = self.generate_deck()

    def generate_deck(self):
        """52枚のカードを生成する。

        Returns:
            list[Card]: シャッフルされたカードのリスト。

        """
        cards = [Card(suit, rank) for rank in Card.VALID_RANKS for suit in Card.VALID_SUITS]
        random.shuffle(cards)
        return cards

    def shuffle(self, cards=None):
        """デッキ内のカードをシャッフルする。

        Args:
            cards (list, optical): カードのリスト。

        """
        if cards is None:
            cards = self.cards
        random.shuffle(cards)
        self.cards = cards

    def draw(self):
        """デッキの一番上のカードを引く。

        Returns:
            Card: 引いたカード。

        """
        return self.cards.pop()
