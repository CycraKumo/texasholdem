from pot import Pot


class MockPlayer:
    def __init__(self, name):
        self.name = name


def test_pot_add_contribution():
    """
    Potクラスの寄与の追加機能をテストします。
    """
    pot = Pot()
    player1 = MockPlayer("Alice")
    player2 = MockPlayer("Bob")

    pot.add_contribution(player1, 100)
    assert pot.total == 100
    assert pot.contributions[player1] == 100
    assert pot.max_contribution == 100

    pot.add_contribution(player2, 200)
    assert pot.total == 300
    assert pot.contributions[player2] == 200
    assert pot.max_contribution == 200


def test_pot_get_contribution():
    """
    Potクラスの寄与額の取得機能をテストします。
    """
    pot = Pot()
    player1 = MockPlayer("Alice")
    player2 = MockPlayer("Bob")

    assert pot.get_contribution(player1) == 0

    pot.add_contribution(player1, 100)
    assert pot.get_contribution(player1) == 100

    pot.add_contribution(player2, 200)
    assert pot.get_contribution(player2) == 200


def test_pot_get_eligible_players():
    """
    Potクラスの資格のあるプレイヤーの取得機能をテストします。
    """
    pot = Pot()
    player1 = MockPlayer("Alice")
    player2 = MockPlayer("Bob")
    player3 = MockPlayer("Charlie")

    pot.add_contribution(player1, 100)
    pot.add_contribution(player2, 200)
    pot.add_contribution(player3, 50)

    eligible_players = pot.get_eligible_players()
    # この場合サイドポット2は受け取れるのはプレイヤー2だけ。
    assert player1 not in eligible_players
    assert player2 in eligible_players
    assert player3 not in eligible_players
