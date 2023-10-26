import pytest

from card import Card
from deck import Deck


def test_deck_initialization():
    """
    Deckクラスの初期化をテストします。

    Tests：
        52枚のカードが正しく生成される。
    """
    deck = Deck()
    assert len(deck.cards) == 52
    assert all(isinstance(card, Card) for card in deck.cards)


def test_deck_shuffle():
    """
    Deckクラスのシャッフル機能をテストします。

    Tests：
        シャッフル前とシャッフル後のデッキの順序が異なる。
        シャッフル後も全てのカードがデッキに含まれている。
    """
    deck = Deck()
    cards_before_shuffle = deck.cards.copy()
    deck.shuffle()
    assert deck.cards != cards_before_shuffle
    assert set(deck.cards) == set(cards_before_shuffle)


def test_deck_draw():
    """
    Deckクラスのカードの引き機能をテストします。

    Tests：
        カードを引くと、デッキのサイズが1つ減少する。
        52枚のカードを全て引いた後、さらにカードを引こうとするとエラーが発生する。
    """
    deck = Deck()
    for _ in range(52):
        card = deck.draw()
        assert isinstance(card, Card)
    with pytest.raises(IndexError):
        deck.draw()
