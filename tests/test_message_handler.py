from message_handler import MessageHandler
from pot import Pot


class MockPlayer:
    def __init__(self, name, chips, hand, bet, db, last_action, position):
        self.name = name
        self.chips = chips
        self.hand = hand
        self.current_bet = bet
        self.is_dealer = db
        self.last_action = last_action
        self.position = position  # Added the missing attribute


def test_message_handler_get_message():
    """
    MessageHandlerクラスのメッセージ取得機能をテストします。
    """
    handler = MessageHandler()

    # Test with an existing key
    handler.get_message("button_holder", player_name="Alice")

    # Test with a non-existing key
    handler.get_message("non_existing_key")

    # Test with format variables
    handler.get_message("win_player", player_name="Bob", get_chips=10, chips=500)


def test_message_handler_display_players_info_modified():
    """
    MessageHandlerクラスのプレイヤー情報の表示機能をテストします。
    """
    handler = MessageHandler()
    players = [
        MockPlayer("Alice", 1000, ["A♥", "K♠"], 200, True, "call", 0),
        MockPlayer("Bob", 900, ["J♦", "Q♦"], 100, False, "fold", 0)
    ]

    handler.display_players_info(players)


def test_message_handler_display_community_cards(capfd):
    """
    MessageHandlerクラスのコミュニティカードの表示機能をテストします。
    """
    handler = MessageHandler()
    community_cards = ["A♥", "K♠", "J♦", "Q♦", "10♠"]
    pots = [Pot()]
    for amount in [100, 200, 300]:
        pots[0].total += amount

    handler.display_community_cards(community_cards, pots[0].total)
    out, err = capfd.readouterr()
    assert "A♥" in out and "K♠" in out and "J♦" in out
    assert "600" in out
