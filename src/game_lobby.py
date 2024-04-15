import random

from game import Game


class GameLobby:
    """ゲームロビーを管理するクラス。

    Attributes:
        message_handler (MessageHandler): メッセージ処理のインスタンス。
        input_handler (InputHandler): 入力処理のインスタンス。
        data_manager (DataManager): セーブデータの管理を行うインスタンス。
        player_name (str): プレイヤー名。
        chips (int): 全体で所持しているチップ数。

    Tests:
        [ ]: test_game_lobby

    """

    # クラス変数を辞書のリストとして初期化
    tables = [
        {'no': '1', 'SB': 1, 'BB': 2, 'bet_type': 'no'},
        {'no': '2', 'SB': 2, 'BB': 4, 'bet_type': 'no'},
        {'no': '3', 'SB': 5, 'BB': 10, 'bet_type': 'no'},
        {'no': '4', 'SB': 1, 'BB': 2, 'bet_type': 'fix'},
        {'no': '5', 'SB': 2, 'BB': 4, 'bet_type': 'fix'},
        {'no': '6', 'SB': 5, 'BB': 10, 'bet_type': 'fix'},
        # {'no': '7', 'SB': 1, 'BB': 2, 'bet_type': 'pot'},
        # {'no': '8', 'SB': 2, 'BB': 4, 'bet_type': 'pot'},
        # {'no': '9', 'SB': 5, 'BB': 10, 'bet_type': 'pot'},
    ]

    def __init__(self, message_handler, input_handler, data_manager, player_name):
        """GameLobbyクラスのインスタンスを初期化する。

        必要なインスタンス変数の初期化や他のクラスのインスタンス化を行う。

        """
        self.message_handler = message_handler
        self.input_handler = input_handler
        self.data_manager = data_manager
        self.player_name = player_name
        self.tables = None

    def display_tables(self):
        """テーブル一覧表示用メソッド

        Tests:
            [ ]: test_display_tables

        """

        # プレイヤーのチップ数を取得、表示
        self.player_data = self.data_manager.get_or_create_user_data(self.player_name)
        self.message_handler.get_message("player_chips", player_name=self.player_name, chips=self.player_data)
        # 自分で立てられる方のテーブルの一覧
        self.message_handler.display_tables_info(GameLobby.tables, 'new', ['No', 'SB-BB', "Bet Type"])

        # すでに立っているテーブルの一覧
        # ランダムに生成するテーブルの数を決定 (3〜5個)
        already_tables = []
        num_of_tables = random.randint(3, 5)

        # bet_type = ['no', 'fix', 'pot']
        bet_type = ['no', 'fix']
        count = len(GameLobby.tables) + 1
        for i in bet_type:
            for j in range(num_of_tables):
                # 新しいテーブル名を生成
                new_table_name = count

                # 新しいテーブルのSBとBBをランダムに設定
                sb = random.choice([1, 2, 5, 10])
                bb = sb * 2

                # テーブルに2〜5人のCPUプレイヤーがいるとする
                num_cpus = random.randint(2, 8)
                cpu_players = self.generate_cpu_players(num_cpus, bb)

                # 新しいテーブルをリストに追加
                already_tables.append({'no': new_table_name, 'SB': sb, 'BB': bb, 'bet_type': i, 'CPUs': cpu_players})
                count += 1

        # テーブル一覧の表示
        self.message_handler.display_tables_info(already_tables, 'already')
        self.tables = already_tables

    def generate_cpu_players(self, num_cpus, bb):
        """ランダムでCPUを作成する

        Args:
            num_cpus (int): CPUの数
            bb (int): BBの値

        Returns:
            list[dict]: CPUとそのCPUが所持しているチップの辞書

        Tests:
            [ ]: test_[テストファイル/メソッド名]

        """
        cpu_players = []
        for _ in range(num_cpus):
            # BBの100倍を基本のチップ数とする
            base_chips = bb * 100
            # チップ数の増減をランダムに決定する（例：1%〜200%の範囲で変動）
            chips_variation = random.randint(1, 200) / 100
            chips = int(base_chips * chips_variation)

            cpu_player = {
                'name': f'CPU{_+1}',
                'chips': chips
            }
            cpu_players.append(cpu_player)
        return cpu_players

    def start_game(self):
        """選択されたテーブルでゲームを開始する。

        Tests:
            [ ]: test_start_game

        """
        # 新規テーブルとすでに立っているテーブルの結合
        selected_table = self.input_handler.select_table(GameLobby.tables + self.tables)

        # テーブルが選択された場合
        if selected_table:
            # テーブルに持ち込むチップ数を取得
            last_chips = self.input_handler.get_initial_chips()

            # テーブルに持ち込むチップ数をセーブデータから減算
            self.data_manager.update_user_data(self.player_name, self.player_data - last_chips)

            # 現在のセーブデータを取得
            self.player_data = self.data_manager.get_or_create_user_data(self.player_name)

            # 選択されたテーブルからCPUs情報を取得
            cpus_info = selected_table.get('CPUs', None)

            # ゲームのインスタンスを生成し、ゲームを開始
            game_instance = Game(self.message_handler, self.input_handler, self.data_manager, self.player_name, last_chips,
                                 sb=selected_table['SB'], bb=selected_table['BB'], bet_type=selected_table['bet_type'], cpus=cpus_info)
            last_chips = game_instance.start_game()

            # ゲームが終了したら、プレイヤーのチップ数をセーブデータに保存
            self.data_manager.update_user_data(self.player_name, self.player_data + last_chips)
            self.player_data = self.data_manager.get_or_create_user_data(self.player_name)

            # プレイヤーのチップ数が0になった場合
            if self.player_data == 0:
                # ゲームを終了する
                return self.player_data, True

        # テーブルが選択されなかった場合
        else:
            # ゲームを終了する
            self.message_handler.get_message("game_exit")
            return self.player_data, True

        # ゲームを続ける
        return self.player_data, False
