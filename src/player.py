import random


class Player:
    """
    プレイヤーの状態を管理するクラス。
    """

    def __init__(self, name, chips, input_handler, is_cpu=False):
        """
        Playerクラスの初期化。

        Parameters:
        - name (str): プレイヤーの名前。
        - chips (int): 初期チップ数。
        - input_handler (InputHandler): 入力クラス。
        - is_cpu (bool): CPUであるかどうか。
        """
        self.name = name
        self.chips = chips
        self.input_handler = input_handler
        self.hand = []
        self.current_bet = 0  # 現在のベット額。
        self.last_action = []  # 最後のアクションを保存する属性
        self.last_bet_amount = 0
        self.is_dealer = False
        self.is_cpu = is_cpu
        self.has_acted = False
        self.is_folded = False  # プレイヤーがフォールドしたかどうかを示すフラグ。
        self.is_all_in = False
        self.hand_category = None
        self.hand_rank = None

    def bet(self, amount):
        """
        プレイヤーがベットするメソッド。指定された額をベットし、所持チップからその額を減少させる。

        Parameters:
        - amount (int): ベットする額。

        Returns:
        - int: 実際にベットされた額。
        """

        actual_bet = min(self.chips, amount)
        self.chips -= actual_bet
        self.current_bet += actual_bet

        return actual_bet

    def fold(self):
        """
        プレイヤーをフォールド状態にします。
        """
        self.hand = []
        self.is_folded = True

    def select_action(self, available_actions):
        """
        利用可能なアクションの中からアクションを選択する。

        Parameters:
        - available_actions (list): 利用可能なアクションのリスト。

        Returns:
        - str: 選択されたアクション。
        """
        return self._cpu_select_action(available_actions) if self.is_cpu else self._player_select_action(available_actions)

    def _cpu_select_action(self, available_actions):
        """
        CPUとしてのアクションを選択する。

        Parameters:
        - available_actions (list): 利用可能なアクションのリスト。

        Returns:
        - str: 選択されたアクション。
        """
        return random.choice(available_actions)

    def _player_select_action(self, available_actions):
        """
        プレイヤーとしてのアクションを選択する。

        Parameters:
        - available_actions (list): 利用可能なアクションのリスト。

        Returns:
        - str: 選択されたアクション。
        """
        return self.input_handler.select_action(available_actions)

    def select_bet_amount(self, min_amount):
        """
        ベットまたはレイズの額を選択する。

        Parameters:
        - min_amount (int): 最小ベット額。

        Returns:
        - int: 選択されたベットまたはレイズの額。
        """
        return self._cpu_select_bet_amount(min_amount) if self.is_cpu else self._player_select_bet_amount(min_amount)

    def _cpu_select_bet_amount(self, min_amount):
        """
        CPUとしてのベットまたはレイズの額を選択する。

        Parameters:
        - min_amount (int): 最小ベット額。

        Returns:
        - int: 選択されたベットまたはレイズの額。
        """
        return random.randint(min_amount, self.chips)

    def _player_select_bet_amount(self, min_amount):
        """
        プレイヤーとしてのベットまたはレイズの額を選択する。

        Parameters:
        - min_amount (int): 最小ベット額。

        Returns:
        - int: 選択されたベットまたはレイズの額。
        """
        return self.input_handler.select_bet_amount(min_amount, self.chips)
