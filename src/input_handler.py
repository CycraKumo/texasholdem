import time


class InputHandler:
    """ユーザーからの入力を処理するクラス。

    Attributes:
        message_handler (MessageHandler): メッセージ処理のインスタンス。

    Tests:
        [ ]: test_input_handler

    """

    def __init__(self, message_handler):
        """InputHandler クラスのコンストラクタ。

        Args:
            message_handler (MessageHandler): メッセージ処理のインスタンス。

        """
        self.message_handler = message_handler

    def get_player_name(self):
        """プレイヤーの名前を入力として取得します。

        Returns:
            str: 入力されたプレイヤーの名前。

        """
        self.message_handler.get_message("user_input")
        return input()

    def get_initial_chips(self):
        """プレイヤーの初期チップ数を入力として取得します。

        Returns:
            int: 入力された初期チップ数。

        """
        while True:
            try:
                self.message_handler.get_message("enter_initial_chips")
                return int(input())
            except ValueError:
                self.message_handler.get_message("invalid_input")

    def select_table(self, tables):
        """プレイするテーブルを入力として取得します。

        Args:
            tables (_type_): _description_

        Returns:
            _type_: _description_

        """
        while True:
            try:
                self.message_handler.get_message("select_table")
                choice = int(input())
                if choice == 0:
                    return None
                selected_table = tables[choice - 1]
                return selected_table
            except (ValueError, IndexError):
                self.message_handler.get_message("invalid_input")

    def get_num_cpu(self):
        """参加するCPUの数を入力として取得します。

        Returns:
            int: 入力されたCPUの数。

        """
        while True:
            try:
                self.message_handler.get_message("enter_num_cpu")
                num_cpu = int(input())
                if 1 <= num_cpu <= 9:
                    return num_cpu
                else:
                    self.message_handler.get_message("invalid_range", min=1, max=9)
            except ValueError:
                self.message_handler.get_message("invalid_input")

    def wait_for_user(self):
        """プレイヤーの入力を待機するメソッド。

        """
        # return input()
        return time.sleep(1.5)

    def continue_to_game(self):
        """ゲームを続けるかやめるかを選択するメソッド。

        """
        while True:
            try:
                self.message_handler.get_message("continue_to_game")
                continue_to_game = int(input())
                if 0 <= continue_to_game <= 1:
                    return continue_to_game
                else:
                    self.message_handler.get_message("invalid_range", min=0, max=1)
            except ValueError:
                self.message_handler.get_message("invalid_input")

    def rebuy_to_game(self):
        """リバイしてゲームを続けるか選択するメソッド。

        """
        while True:
            try:
                self.message_handler.get_message("rebuy_chips")
                return int(input())
            except ValueError:
                self.message_handler.get_message("invalid_input")

    def select_action(self, available_actions):
        """利用可能なアクションの中からアクションを選択する。

        Args:
            available_actions (list[str]): 選択可能なアクションのリスト。

        Returns:
            str: 選択されたアクション。

        """
        available_actions_list = []
        for i, action in enumerate(available_actions):
            available_actions_list.append(f"{i}: {action}")

        while True:
            self.message_handler.get_message("choose_action", available_actions=', '.join(available_actions_list))
            selected_index = input().lower()
            if selected_index.isdigit() and 0 <= int(selected_index) < len(available_actions):
                return available_actions[int(selected_index)]
            else:
                self.message_handler.get_message("invalid_action")

    def select_bet_amount(self, min_amount, max_amount):
        """ベットまたはレイズの額を選択する。

        Args:
            min_amount (int): 最小ベット、またはレイズ額。
            max_amount (int): 最大ベット、またはレイズ額。

        Returns:
            int: 選択されたベット、またはレイズ額。

        """
        while True:
            self.message_handler.get_message("enter_bet_amount", min_amount=min_amount, max_amount=max_amount)
            amount = int(input())
            if min_amount <= amount <= max_amount:
                return amount
            else:
                self.message_handler.get_message("invalid_bet_amount", min_amount=min_amount, max_amount=max_amount)
