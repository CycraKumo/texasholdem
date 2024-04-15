from dealer import Dealer
from message_handler import MessageHandler
from input_handler import InputHandler


def test_dealer_initialization():
    """
    Dealerクラスの初期化をテストします。

    Tests:

    """
    message_handler = MessageHandler()
    input_handler = InputHandler(message_handler)
    dealer = Dealer(message_handler, input_handler)
    print(dealer)
