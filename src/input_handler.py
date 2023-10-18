class InputHandler:
    """
    ユーザーからの入力を処理するクラス。
    """

    def __init__(self, message_handler):
        """
        InputHandler クラスのコンストラクタ。

        Parameters:
        - message_handler (MessageHandler): メッセージ処理のインスタンス。
        """
        self.message_handler = message_handler

    def get_player_name(self):
        """
        プレイヤーの名前を入力として取得します。

        Returns:
        - str: 入力されたプレイヤーの名前。
        """
        return input(self.message_handler.get_message("enter_player_name"))

    def get_game_mode(self):
        """
        ゲームモードを入力として取得します。

        Returns:
        - int: 入力されたゲームモード。
        """
        while True:
            try:
                num_cpu = int(input(self.message_handler.get_message("enter_game_mode")))
                if 1 <= num_cpu <= 2:
                    return num_cpu
                else:
                    print(self.message_handler.get_message("invalid_range", min=1, max=2))
            except ValueError:
                print(self.message_handler.get_message("invalid_input"))

    def get_initial_chips(self):
        """
        プレイヤーの初期チップ数を入力として取得します。

        Returns:
        - int: 入力された初期チップ数。
        """
        while True:
            try:
                return int(input(self.message_handler.get_message("enter_initial_chips")))
            except ValueError:
                print(self.message_handler.get_message("invalid_input"))

    def get_num_cpu(self):
        """
        参加するCPUの数を入力として取得します。

        Returns:
        - int: 入力されたCPUの数。
        """
        while True:
            try:
                num_cpu = int(input(self.message_handler.get_message("enter_num_cpu")))
                if 1 <= num_cpu <= 9:
                    return num_cpu
                else:
                    print(self.message_handler.get_message("invalid_range", min=1, max=9))
            except ValueError:
                print(self.message_handler.get_message("invalid_input"))

    def wait_for_user(self):
        """
        プレイヤーの入力を待機するメソッド。
        """
        return input()

    def select_action(self, available_actions):
        """
        利用可能なアクションの中からアクションを選択する。

        Parameters:
        - available_actions (list): 選択可能なアクションのリスト。

        Returns:
        - str: 選択されたアクション。
        """

        available_actions_list = []
        for i, action in enumerate(available_actions):
            available_actions_list.append(f"{i}: {action}")

        while True:
            selected_index = input(self.message_handler.get_message("choose_action", available_actions=', '.join(available_actions_list))).lower()
            if selected_index.isdigit() and 0 <= int(selected_index) < len(available_actions):
                return available_actions[int(selected_index)]
            else:
                print(self.message_handler.get_message("invalid_action"))

    def select_bet_amount(self, min_amount, max_amount):
        """
        ベットまたはレイズの額を選択する。
        """
        while True:
            amount = int(input(self.message_handler.get_message("enter_bet_amount", min_amount=min_amount, max_amount=max_amount)))
            if min_amount <= amount <= max_amount:
                return amount
            else:
                print(self.message_handler.get_message("invalid_bet_amount", min_amount=min_amount, max_amount=max_amount))
