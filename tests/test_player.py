from player import Player


class MockInputHandler:
    def get_input(self, prompt):
        # For simplicity, always returning 'call' for action and '10' for bet amount.
        return 'call' if 'action' in prompt else '10'

    def select_action(self, available_actions):
        # For simplicity, always return 'call' if it's an available action.
        return 'call' if 'call' in available_actions else available_actions[0]

    def select_bet_amount(self, min_amount, max_amount):
        # For simplicity, always return the min_amount.
        return min_amount


def test_player_initialization():
    """
    Playerクラスの初期化をテストします。
    """
    player = Player("Alice", 1000, MockInputHandler(), is_cpu=False)
    assert player.name == "Alice"
    assert player.chips == 1000
    assert not player.is_cpu
    assert isinstance(player.input_handler, MockInputHandler)


def test_player_bet():
    """
    Playerクラスのベット機能をテストします。
    """
    player = Player("Alice", 1000, MockInputHandler(), is_cpu=False)
    player.bet(200)
    assert player.chips == 800
    assert player.current_bet == 200
    # Bet more than available chips
    player.bet(1000)
    assert player.chips == 0


def test_player_fold():
    """
    Playerクラスのフォールド機能をテストします。
    """
    player = Player("Alice", 1000, MockInputHandler(), is_cpu=False)
    player.fold()
    assert player.is_folded


def test_player_select_action():
    """
    Playerクラスのアクションの選択機能をテストします。
    """
    player_cpu = Player("Bob", 1000, MockInputHandler(), is_cpu=True)
    assert player_cpu.select_action(['call', 'raise', 'fold']) in ['call', 'raise', 'fold']

    player_human = Player("Alice", 1000, MockInputHandler(), is_cpu=False)
    assert player_human.select_action(['call', 'raise', 'fold']) == 'call'


def test_player_select_bet_amount():
    """
    Playerクラスのベット額の選択機能をテストします。
    """
    player_cpu = Player("Bob", 1000, MockInputHandler(), is_cpu=True)
    assert 0 <= player_cpu.select_bet_amount(10) <= 1000

    player_human = Player("Alice", 1000, MockInputHandler(), is_cpu=False)
    assert player_human.select_bet_amount(10) == 10
