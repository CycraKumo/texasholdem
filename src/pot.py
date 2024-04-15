class Pot:
    """
    ゲーム内のポットを管理するクラス。

    Attributes:
        total (int): ポットにあるチップの合計。
        contributions (dict[str, int]): プレイヤーごとのチップの寄与額。
        max_contribution (int): このポットに対する最大寄与額。

    Tests:
        [ ]: test_pot

    """

    def __init__(self):
        """Potクラスの初期化。

        """
        self.total = 0
        self.contributions = {}
        self.max_contribution = 0

    def add_contribution(self, player, amount):
        """プレイヤーからの指定された量の寄与を追加する。

        Args:
            player (str): プレイヤーの名前。
            amount (int): 寄与する額。

        """
        self.total += amount
        self.contributions[player] = self.contributions.get(player, 0) + amount
        self.max_contribution = max(self.max_contribution, amount)

    def get_contribution(self, player):
        """指定されたプレイヤーの寄与額を返す。

        Args:
            player (str): プレイヤーの名前。

        Returns:
            int: プレイヤーの寄与額。

        """
        return self.contributions.get(player, 0)

    def get_eligible_players(self):
        """このポットを獲得する資格があるプレイヤーのリストを返す。

        Returns:
            list[Player]: 資格があるプレイヤーのリスト。

        """
        return [player for player, amount in self.contributions.items() if amount >= self.max_contribution]
