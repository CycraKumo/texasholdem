class Pot:
    """
    ゲーム内のポットを管理するクラス。

    Attributes:
    - total (int): ポットにあるチップの合計。
    - contributions (dict): プレイヤーごとのチップの寄与額。
    - max_contribution (int): このポットに対する最大寄与額。

    Methods:
    - add_contribution(player, amount): プレイヤーからの寄与を追加する。
    - get_contribution(player): プレイヤーの寄与額を取得する。
    - get_eligible_players(): このポットを獲得する資格があるプレイヤーのリストを返す。
    """

    def __init__(self):
        """
        Potクラスの初期化。
        """
        self.total = 0
        self.contributions = {}
        self.max_contribution = 0

    def add_contribution(self, player, amount):
        """
        プレイヤーからの指定された量の寄与を追加する。

        Parameters:
        - player (str): プレイヤーの名前。
        - amount (int): 寄与する額。
        """
        self.total += amount
        self.contributions[player] = self.contributions.get(player, 0) + amount
        self.max_contribution = max(self.max_contribution, amount)

    def get_contribution(self, player):
        """
        指定されたプレイヤーの寄与額を返す。

        Parameters:
        - player (str): プレイヤーの名前。

        Returns:
        - int: プレイヤーの寄与額。
        """
        return self.contributions.get(player, 0)

    def get_eligible_players(self):
        """
        このポットを獲得する資格があるプレイヤーのリストを返す。

        Returns:
        - list: 資格があるプレイヤーのリスト。
        """
        return [player for player, amount in self.contributions.items() if amount >= self.max_contribution]
