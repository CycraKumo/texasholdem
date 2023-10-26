class MessageHandler:
    """
    ゲーム内のメッセージを管理するクラス。

    Attributes:
        messages (dict[str, str]): 表示する文言の一覧。

    Tests:
        [ ]: test_message_manager

    """

    def __init__(self):
        """MessageHandler クラスのコンストラクタ。

        """
        self.messages = {
            "user_list": "ユーザー一覧",
            "user_input": "ユーザー名を入力してください:",
            "welcome_user": "ようこそ, {user_name}!",
            "now_chips": "現在のチップ: {chips}",
            "add_user": "{user_name} として新規登録します。",
            "initial_chips": "初期チップ: {initial_chips} が付与されました。",
            "enter_player_name": "プレイヤーの名前を入力してください: ",
            "enter_game_mode": "ゲームモードを選択してください 1:リミット 2:ポットリミット 3:ノーリミット : ",
            "enter_initial_chips": "ゲームに持ち込むチップの数を入力してください: ",
            "enter_num_cpu": "参加するCPUの数を入力してください: ",
            "invalid_input": "無効な入力です。もう一度入力してください。",
            "invalid_range": "無効な範囲です。{min}～{max}の範囲で入力して下さい。",
            "set_initial_button": "ディーラーボタンの位置を決定中...",
            "button_holder": "{player_name}がディーラーボタンを獲得。",
            "choose_action": "利用可能なアクション: {available_actions}\nアクションを選択してください(数値で入力):",
            "invalid_action": "無効なアクションです。もう一度選択してください。",
            "enter_bet_amount": "{min_amount} から {max_amount} までのベット額を入力してください:",
            "invalid_bet_amount": "無効なベット額です。{min_amount} から {max_amount} までの間で入力してください。",
            "community_cards": "コミュニティカード: ",
            "pots": "ポット: {pots}",
            "best_hand": "\nプレイヤーのベストハンド:",
            "player_best_hand": "{player_name} - ハンドカテゴリ: {hand_category}, ランク: {hand_rank}\n",
            "win_player": "{player_name} - チップ獲得: {get_chips} → 合計: {chips}\n",
            "main_pot": "メインポット勝者",
            "side_pot": "サイドポット{index}勝者",
            "continue_to_game": "0: つづける 1: やめる : "
            # 他のメッセージも必要に応じて追加してください
        }

    def get_message(self, key, **kwargs):
        """キーに対応するメッセージを返す。必要に応じて文字列のフォーマットも行う。

        Args:
            key (str): メッセージのキー。
            ``**kwarg``: フォーマット用の変数。

        Returns:
            str: 対応するメッセージ。

        """
        return self.messages.get(key, "メッセージが見つかりません。").format(**kwargs)

    def display_players_info(self, players, columns_to_display=["PlayerName", "Chips", "Hand", "Bet", "DB", "Action"]):
        """プレイヤーの情報をカスタマイズされた表形式で表示する。

        Args:
            players (list[Player]): Playerクラスのインスタンスのリスト。
            columns_to_display (list[str]): 表示したい項目のリスト。Noneの場合はすべて表示。

        Returns:
            str: プレイヤー情報の表。

        """
        # カラム毎の最大長さ導出
        column_max_widths = {}

        if "PlayerName" in columns_to_display:
            column_max_widths["PlayerName"] = max(
                len("PlayerName"),
                max(len(player.name) + sum(1 for ch in player.name if ord(ch) > 127) for player in players)
            )

        if "Chips" in columns_to_display:
            column_max_widths["Chips"] = max(len("Chips"), max(len(str(player.chips)) for player in players))

        if "Hand" in columns_to_display:
            column_max_widths["Hand"] = max(len("Hand"), max(len(", ".join([str(card) for card in player.hand])) for player in players))

        if "Bet" in columns_to_display:
            column_max_widths["Bet"] = max(len("Bet"), max(len(str(player.current_bet)) for player in players))

        if "DB" in columns_to_display:
            column_max_widths["DB"] = 3  # "○" or " " のどちらかなので、常に3とします

        if "Action" in columns_to_display:
            column_max_widths["Action"] = max(
                len("Action"),
                max(
                    len(f"{player.last_action[-1] if player.last_action else ''}: {player.last_bet_amount}")
                    if player.last_action and player.last_action[-1] in ["Bet", "Raise"]
                    else len(player.last_action[-1] if player.last_action else '')
                    for player in players
                )
            )

        # ヘッダー部分の表示
        header = "+"
        for column in columns_to_display:
            header += "-" * (column_max_widths[column] + 2) + "+"
        header += "\n"

        header_names = "|"
        for column in columns_to_display:
            header_names += f" {column:<{column_max_widths[column]}} |"
        header_names += "\n"

        header += header_names
        header += "+"
        for column in columns_to_display:
            header += "-" * (column_max_widths[column] + 2) + "+"
        header += "\n"

        # 各プレイヤーの情報を表示する部分
        body = ""
        for player in players:
            line = "|"
            if "PlayerName" in columns_to_display:
                padding_space = column_max_widths['PlayerName'] - len(player.name) - sum(1 for ch in player.name if ord(ch) > 127)
                line += f" {player.name}{' ' * padding_space} |"
            if "Chips" in columns_to_display:
                line += f" {player.chips:<{column_max_widths['Chips']}} |"
            if "Hand" in columns_to_display:
                hand = ", ".join([str(card) for card in player.hand])
                line += f" {hand:<{column_max_widths['Hand']}} |"
            if "Bet" in columns_to_display:
                line += f" {player.current_bet:<{column_max_widths['Bet']}} |"
            if "DB" in columns_to_display:
                db = "○" if player.is_dealer else " "
                line += f" {db:^3} |"
            if "Action" in columns_to_display:
                if player.last_action and player.last_action[-1] in ["Bet", "Raise"]:
                    action = f"{player.last_action[-1]}: {player.last_bet_amount}"
                else:
                    action = player.last_action[-1] if player.last_action else ""
                line += f" {action:<{column_max_widths['Action']}} |"
            body += line + "\n"

        # フッター部分の表示
        footer = "+"
        for column in columns_to_display:
            footer += "-" * (column_max_widths[column] + 2) + "+"
        footer += "\n"

        # 全体のテーブルを組み合わせ、リターンする
        return header + body + footer

    def display_community_cards(self, community_cards, pots):
        """コミュニティカードとポットの情報を表示する。

        Args:
            community_cards (list[Card]): コミュニティカードとして表示するカードのリスト。
            pot (int): ポットの現在の合計額。

        """
        print(self.get_message("community_cards"), end=" ")
        for card in community_cards:
            print(card, end=" ")
        print("\n" + "-"*30)
        print(self.get_message("pots", pots=pots),  end=" ")
        print("\n" + "-"*30)
