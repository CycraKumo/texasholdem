from unittest.mock import patch

from input_handler import InputHandler
from message_handler import MessageHandler

message = MessageHandler()


def test_get_player_name():
    """
    get_player_nameメソッドのテスト。
    """
    handler = InputHandler(message)

    with patch('builtins.input', return_value='Alice'):
        name = handler.get_player_name()
    assert name == 'Alice'


def test_get_initial_chips():
    """
    get_initial_chipsメソッドのテスト。
    """
    handler = InputHandler(message)

    with patch('builtins.input', return_value='1000'):
        chips = handler.get_initial_chips()
    assert chips == 1000


def test_get_num_cpu():
    """
    get_num_cpuメソッドのテスト。
    """
    handler = InputHandler(message)

    with patch('builtins.input', return_value='3'):
        num = handler.get_num_cpu()
    assert num == 3


def test_select_action():
    """
    select_actionメソッドのテスト。
    """
    handler = InputHandler(message)
    available_actions = ["fold", "call", "raise"]

    with patch('builtins.input', return_value='2'):
        action = handler.select_action(available_actions)
    assert action == "raise"


def test_select_bet_amount():
    """
    select_bet_amountメソッドのテスト。
    """
    handler = InputHandler(message)

    with patch('builtins.input', return_value='200'):
        amount = handler.select_bet_amount(100, 500)
    assert amount == 200
