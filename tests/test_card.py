from card import Card


def test_card_initialization():
    """
    Cardクラスの初期化をテストします。

    以下の内容をテストします：
    - 有効なスートとランクでの正しい初期化。
    - 無効なスートを指定した場合のエラー発生。
    - 無効なランクを指定した場合のエラー発生。
    """
    # 有効なスートとランク
    card = Card("♤", "A")
    assert card.suit == "♤"
    assert card.rank == "A"


def test_card_str_representation():
    """
    Cardクラスの文字列表現をテストします。

    以下の内容をテストします：
    - さまざまなスートとランクの組み合わせでの正しい文字列表現。
    """
    card1 = Card("♤", "A")
    assert str(card1) == " A ♤"

    card2 = Card("♡", "10")
    assert str(card2) == "10 ♡"

    card3 = Card("♢", "K")
    assert str(card3) == " K ♢"

    card4 = Card("♧", "5")
    assert str(card4) == " 5 ♧"
