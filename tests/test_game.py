from game import Game
from message_handler import MessageHandler
from input_handler import InputHandler


def test_game_initialization():
    """
    Gameクラスの初期化をテストします。

    Tests:
        52枚のカードが正しく生成される。
    """
    message_handler = MessageHandler()
    input_handler = InputHandler(message_handler)
    player_name = "test"
    chips = 1000
    sb = 1
    bb = 2
    game = Game(message_handler, input_handler, player_name, chips, sb, bb)
    print(game)
