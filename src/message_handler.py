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
            "args": "{args}",
            "user_list": "ユーザー一覧",
            "user_input": "ユーザー名を入力してください:",
            "player_chips": "プレイヤー名: {player_name} チップ数: {chips}",
            "table_detail": "{table_name}: {sb}-{bb}",
            "select_table": "テーブル番号を選択してください(または0で終了):",
            "abst_table": "テーブル一覧:\n-----------------\n'新規' テーブルはプレイヤーとCPUのチップ数が同じ状態で始まります。\n'既存' テーブルはプレイヤーとCPUのチップ数に差がある状態で始まります。",
            "welcome_user": "ようこそ, {user_name}!",
            "now_chips": "現在のチップ: {chips}",
            "add_user": "{user_name} として新規登録します。",
            "initial_chips": "初期チップ: {initial_chips} が付与されました。",
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
            "remove_cpu": "{player_name}が席を立ちました。",
            "rebuy_cpu": "{player_name}が、チップを{initial_chips}にリバイしました。",
            "continue_to_game": "0: つづける 1: やめる : ",
            "zero_chips": "所持チップが0になりました",
            "rebuy_chips": "リバイする場合、新たに持ち込むチップ数を入力(0の場合は席を立つ):",
            "game_exit": "ゲーム終了。お疲れ様でした。",
            # 他のメッセージも必要に応じて追加してください
        }

    def get_message(self, key, **kwargs):
        """キーに対応するメッセージを返す。必要に応じて文字列のフォーマットも行う。

        Args:
            key (str): メッセージのキー。
            ``**kwarg``: フォーマット用の変数。

        """
        print(self.messages.get(key, "メッセージが見つかりません。").format(**kwargs))

    def display_tables_info(self, tables, status, columns_to_display=["No", "SB-BB", "Bet Type", "CPU Players", "Total Chips"]):
        """テーブルの情報をカスタマイズされた表形式で表示する。

        Args:
            tables (list[dict]): テーブル情報を含む辞書のリスト。
            columns_to_display (list[str]): 表示したい項目のリスト。Noneの場合はすべて表示。
        """
        # 説明
        if status == 'new':
            self.get_message("abst_table")
        abst = "+------+\n"
        if status == 'new':
            abst += "| 新規 |\n"
        else:
            abst += "| 既存 |\n"
        abst += "+------+\n"
        # カラム毎の最大長さ導出
        column_max_widths = {}

        for column in columns_to_display:
            if column == "No":
                column_max_widths[column] = max(len(column), max(len(str(table['no'])) for table in tables))
            elif column == "SB-BB":
                column_max_widths[column] = max(len(column), max(len(f"{table['SB']}-{table['BB']}") for table in tables))
            elif column == "Bet Type":
                column_max_widths[column] = max(len(column), max(len(f"{table['bet_type']}") for table in tables))
            elif column == "CPU Players":
                # CPUプレイヤーの数を正確に計算
                column_max_widths[column] = max(len(column), max(len(str(len(table['CPUs']))) for table in tables))
            elif column == "Total Chips":
                # CPUプレイヤーのチップ合計を正確に計算
                column_max_widths[column] = max(len(column), max(len(str(sum(cpu['chips'] for cpu in table['CPUs']))) for table in tables))

        # ヘッダー部分の表示
        header = "+"
        for column in columns_to_display:
            header += "-" * (column_max_widths[column] + 2) + "+"
        header += "\n"

        header_names = "|"
        for column in columns_to_display:
            header_names += f" {column:{column_max_widths[column]}} |"
        header_names += "\n"

        header += header_names
        header += "+"
        for column in columns_to_display:
            header += "-" * (column_max_widths[column] + 2) + "+"
        header += "\n"

        # 各テーブルの情報を表示する部分
        body = ""
        for table in tables:
            line = "|"
            if "No" in columns_to_display:
                line += f" {table['no']:{column_max_widths['No']}} |"
            if "SB-BB" in columns_to_display:
                sb_bb = f"{table['SB']}-{table['BB']}"
                line += f" {sb_bb:{column_max_widths['SB-BB']}} |"
            if "Bet Type" in columns_to_display:
                line += f" {table['bet_type']:{column_max_widths['Bet Type']}} |"
            if "CPU Players" in columns_to_display:
                # CPUプレイヤーの数を表示
                cpu_players = len(table['CPUs'])
                line += f" {cpu_players:{column_max_widths['CPU Players']}} |"
            if "Total Chips" in columns_to_display:
                # CPUプレイヤーのチップ合計を表示
                total_chips = sum(cpu['chips'] for cpu in table['CPUs'])
                line += f" {total_chips:{column_max_widths['Total Chips']}} |"
            body += line + "\n"

        # フッター部分の表示
        footer = "+"
        for column in columns_to_display:
            footer += "-" * (column_max_widths[column] + 2) + "+"
        footer += "\n"

        # 全体のテーブルを組み合わせ、表示する
        print(abst + header + body + footer)

    def display_players_info(self, players, columns_to_display=["PlayerName", "Chips", "Hand", "Bet", "DB", "Action"]):
        """プレイヤーの情報をカスタマイズされた表形式で表示する。

        Args:
            players (list[Player]): Playerクラスのインスタンスのリスト。
            columns_to_display (list[str]): 表示したい項目のリスト。Noneの場合はすべて表示。

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
        print(header + body + footer)

    def display_community_cards(self, community_cards, pots):
        """コミュニティカードとポットの情報を表示する。

        Args:
            community_cards (list[Card]): コミュニティカードとして表示するカードのリスト。
            pot (int): ポットの現在の合計額。

        """
        self.get_message("community_cards")
        for card in community_cards:
            print(card, end=" ")
        print("\n" + "-"*30)
        self.get_message("pots", pots=pots)
        print("\n" + "-"*30)
