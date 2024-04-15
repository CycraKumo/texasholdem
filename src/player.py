import random


class Player:
    """
    プレイヤーの状態を管理するクラス。

    Attributes:
        name (str): プレイヤーの名前。
        chips (str): プレイヤーが所持しているチップ
        input_handler (InputHandler): 入力処理のインスタンス。
        hand (list[Card]): プレイヤーが所持しているハンド。
        current_bet (int): プレイヤーが現在かけている金額。
        last_action (list[str]): プレイヤーが行ったアクションの一覧。
        is_dealer (bool): ディーラーボタンの所持フラグ。
        is_cpu (bool, optical): CPUであるかどうか。
        has_acted (bool): そのラウンド中アクションをする必要がないかのフラグ。
        is_folded (bool): フォールドしているかのフラグ。
        is_all_in (bool): オール・インしているかのフラグ。
        hand_category (HandCategory): プレイヤーが所持している手のカテゴリ。
        hand_rank (list[int]): プレイヤーが所持している手のランク。

    Tests:
        [ ]: test_player

    """

    def __init__(self, name, chips, input_handler, is_cpu=False):
        """Playerクラスの初期化。

        Args:
            name (str): プレイヤーの名前。
            chips (int): 初期チップ数。
            input_handler (InputHandler): 入力クラス。
            is_cpu (bool, optical): CPUであるかどうか。

        """
        self.name = name
        self.chips = chips
        self.input_handler = input_handler
        self.hand = []
        self.current_bet = 0  # 現在のベット額。
        self.last_action = []  # 最後のアクションを保存する属性
        self.is_dealer = False
        self.is_cpu = is_cpu
        self.has_acted = False
        self.is_folded = False  # プレイヤーがフォールドしたかどうかを示すフラグ。
        self.is_all_in = False
        self.hand_category = None
        self.hand_rank = None
        self.rebuy_count = 0

    def bet(self, amount):
        """プレイヤーがベットするメソッド。

        指定された額をベットし、所持チップからその額を減少させる。

        Args:
            amount (int): ベットする額。

        Returns:
            int: 実際にベットされた額。

        """
        actual_bet = min(self.chips, amount)
        self.chips -= actual_bet
        self.current_bet += actual_bet

        return actual_bet

    def fold(self):
        """プレイヤーをフォールド状態にする。
        """
        self.hand = []
        self.is_folded = True

    def select_action(self, available_actions):
        """利用可能なアクションの中からアクションを選択する。

        Args:
            available_actions (list[str]): 利用可能なアクションのリスト。

        Returns:
            str: 選択されたアクション。

        """
        action = ""
        if self.is_cpu:
            action = self._cpu_select_action(available_actions)
        else:
            action = self._player_select_action(available_actions)
        return action

    def _cpu_select_action(self, available_actions):
        """CPUとしてのアクションを選択する。

        Args:
            available_actions (list): 利用可能なアクションのリスト。

        Returns:
            str: 選択されたアクション。

        """
        return random.choice(available_actions)

    def _player_select_action(self, available_actions):
        """プレイヤーとしてのアクションを選択する。

        Args:
            available_actions (list[str]): 利用可能なアクションのリスト。

        Returns:
            str: 選択されたアクション。

        """
        return self.input_handler.select_action(available_actions)

    def select_bet_amount(self, min_amount, max_amount):
        """ベットまたはレイズの額を選択する。

        Args:
            min_amount (int): 最小ベット額。
            max_amount (int): 最大ベット額

        Returns:
            int: 選択されたベットまたはレイズの額。

        """
        return self._cpu_select_bet_amount(min_amount, max_amount) if self.is_cpu else self._player_select_bet_amount(min_amount, max_amount)

    def _cpu_select_bet_amount(self, min_amount, max_amount):
        """CPUとしてのベットまたはレイズの額を選択する。

        Args:
            min_amount (int): 最小ベット額。

        Returns:
            int: 選択されたベットまたはレイズの額。

        """
        return random.randint(min_amount, max_amount)

    def _player_select_bet_amount(self, min_amount, max_amount):
        """プレイヤーとしてのベットまたはレイズの額を選択する。

        Args:
            min_amount (int): 最小ベット額。

        Returns:
            int: 選択されたベットまたはレイズの額。

        """
        return self.input_handler.select_bet_amount(min_amount, max_amount)
