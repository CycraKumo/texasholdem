import random

from player import Player
from table import Table


class Game:
    """メインロジックを管理するクラス。

    Attributes:
        message_handler (MessageHandler): メッセージ処理のインスタンス。
        input_handler (InputHandler): 入力処理のインスタンス。
        dealer (Dealer): ディーラークラスのインスタンス。
        player_name (str): プレイヤー名。
        chips (int): ゲームに持ち込むチップ数。
        sb (int): SBの額。
        bb (int): BBの額。
        cpus (list[dict]): CPUの状態。

    Tests:
        [ ]: test_game

    """

    def __init__(self, message_handler, input_handler, data_manager, player_name, chips, bet_type, sb, bb, cpus=None):
        """Gameクラスのインスタンスを初期化する。

        必要なインスタンス変数の初期化や他のクラスのインスタンス化を行う。

        Args:
            message_handler (MessageHandler): メッセージ処理のインスタンス。
            input_handler (InputHandler): 入力処理のインスタンス。
            dealer (Dealer): ディーラークラスのインスタンス。
            player_name (str): プレイヤー名。
            chips (int): ゲームに持ち込むチップ数。
            sb (int): SBの額。
            bb (int): BBの額。
            cpus (list[dict]): CPUの状態。

        """
        self.message_handler = message_handler
        self.input_handler = input_handler
        self.data_manager = data_manager
        self.table = Table(self.message_handler, self.input_handler)
        self.player_name = player_name
        self.chips = chips
        self.bet_type = bet_type
        self.sb = sb
        self.bb = bb
        self.cpus = cpus

    def start_game(self):
        """ゲームを開始する。

        ゲームの開始時の前処理とメイン処理を順に実行する。

        """
        self.pre_process()
        while True:
            last_chips = 0
            end_flg = False
            last_chips, end_flg = self.main_process()
            if end_flg:
                break

        return last_chips

    def pre_process(self):
        """ゲーム開始前の処理を行う。

        例: プレイヤーの登録、初期配置のセットアップなど

        """

        # プレイヤーインスタンスの生成
        self.players = [Player(name=self.player_name, chips=self.chips, input_handler=self.input_handler)]

        # CPUの人数の入力 ここテーブルによって分岐処理が入る
        if self.cpus is None:
            num_cpu = self.input_handler.get_num_cpu()
            for i in range(num_cpu):
                self.players.append(Player(name=f"CPU{i+1}", chips=self.chips,
                                           input_handler=self.input_handler, is_cpu=True))
        else:
            for cpu in self.cpus:
                self.players.append(Player(name=cpu['name'], chips=cpu['chips'],
                                           input_handler=self.input_handler, is_cpu=True))

        # ランダムに席につかせる
        random.shuffle(self.players)

        # ディーラーボタン配置の決定
        self.message_handler.get_message("set_initial_button")
        self.input_handler.wait_for_user()
        button_holder = self.table.dealer.set_initial_button(self.players)
        self.message_handler.get_message("button_holder", player_name=button_holder.name)
        self.input_handler.wait_for_user()

        # プレイヤー情報の表示
        self.display_game_state()

    def collect_blinds(self):
        """Small BlindとBig Blindを徴収します。

        """
        # ボタンの位置を取得
        dealer_position = next(i for i, player in enumerate(self.players) if player.is_dealer)
        # SBとBBの位置を計算
        sb_position = (dealer_position + 1) % len(self.players)
        bb_position = (dealer_position + 2) % len(self.players)

        # SBとBBのプレイヤーを取得
        sb_player = self.players[sb_position]
        bb_player = self.players[bb_position]

        self.sb_amount = self.sb  # ここは任意のSBの額を設定できます。
        self.bb_amount = self.bb  # ここは任意のBBの額を設定できます。

        # SBとBBの徴収
        sb_player.bet(self.sb_amount)
        bb_player.bet(self.bb_amount)

        self.table.dealer.bet_record.append(self.sb_amount)
        self.table.dealer.bet_record.append(self.bb_amount)

        # プレイヤー情報の表示
        self.display_game_state()

    def display_game_state(self):
        """ゲームの現在の状態を表示します。

        プレイヤー情報、コミュニティカードなど

        """
        # コミュニティカードの情報
        self.message_handler.display_community_cards(self.table.dealer.community_cards, sum(pot.total for pot in self.table.dealer.pots))

        # プレイヤー情報
        self.message_handler.display_players_info(self.players)

        # ユーザーからの入力待機
        self.input_handler.wait_for_user()

    def main_process(self):
        """ゲームのメインロジックを実行する。

        プリフロップ、フロップ、ターン、リバーなどの各段階での処理を行う。

        """
        # デッキの作り直し
        self.table.dealer.deck.generate_deck()

        # SBとBBの徴収
        self.collect_blinds()

        # 各プレイヤーに２枚ずつカードを配る
        self.table.dealer.deal_hole_cards(self.players)

        # プレイヤー情報の表示
        self.display_game_state()

        # ベットラウンド開始
        # コミュニティカードをめくる枚数
        community_cards_dict = {
            "flop": 3,
            "turn": 1,
            "river": 1
        }

        # プリフロップの開始
        remaining_players = self.table.dealer.bet_round(self.players, self.bb_amount, self.bb, self.bet_type, bet_round='pre_flop')

        # 賭け金をポットに移動。その他bet_round関数で設定した値の初期化処理
        self.table.dealer.pot_collect(self.players)

        # プレイヤー情報の表示
        self.display_game_state()

        if len(remaining_players) > 1:

            for key, num_cards in community_cards_dict.items():

                # コミュニティカードをめくる
                self.table.dealer.reveal_community_cards(num_cards)

                # プレイヤー情報の表示
                self.display_game_state()

                # フロップ、ターン、リバーベッティングラウンドを開始
                remaining_players = self.table.dealer.bet_round(self.players, self.bb_amount, self.bb, self.bet_type, bet_round=key)

                # 賭け金をポットに移動。その他bet_round関数で設定した値の初期化処理
                self.table.dealer.pot_collect(self.players)

                # プレイヤー情報の表示
                self.display_game_state()

                if len(remaining_players) == 1:
                    break

        # ここまででlen(remaining_players)が2以上なら、アクティブなプレイヤーで手の強さ比べを行う
        if len(remaining_players) > 1:
            self.table.dealer.evaluate_and_fold_players(remaining_players)
        else:
            self.table.dealer.distribute_pot(remaining_players)

        # CPUのチップ数が0になった場合
        # リバイするか、その席を抜けるか。playerclassでリバイ数を管理して、負けが増えるほど席を立つ確率が上がる
        for player in self.players:
            if player.is_cpu:
                if player.chips == 0:
                    leave_probability = player.rebuy_count / 5
                    if random.random() < leave_probability:
                        self.message_handler.get_message("remove_cpu", player_name=player.name)
                        self.players.remove(player)
                    else:
                        self.message_handler.get_message("rebuy_cpu", player_name=player.name, initial_chips=self.chips)
                        player.chips = self.chips
                        player.rebuy_count += 1

        # プレイヤーのチップ数が0になった場合は自動で返す。
        # プレイヤーのリバイ処理をここで行う
        target_players = [player for player in self.players if player.name == self.player_name]
        if target_players[0].chips == 0:
            # チップが0になったことを表示する
            self.message_handler.get_message("zero_chips")

            # リバイするか聞く
            rebuy_chips = self.input_handler.rebuy_to_game()

            if rebuy_chips == 0:
                return 0, True
            else:
                target_players[0].chips = rebuy_chips
                # テーブルに持ち込むチップ数をセーブデータから減算
                player_data = self.data_manager.get_or_create_user_data(self.player_name)
                self.data_manager.update_user_data(self.player_name, player_data - rebuy_chips)
        else:
            # ユーザーからの入力待機
            continue_to_game = self.input_handler.continue_to_game()
            if continue_to_game == 1:
                # ゲーム終了。現在のチップを返す。
                return target_players[0].chips, True

        # めちゃくちゃ少ない確率で新たなCPUが追加される。または席を立つ。
        # 入ってくるのは初期チップ

        # 席にいる人が1人になった場合（プレイヤーのみになった場合）
        # その席をバラす（lobbyに戻る）
        if len(self.players) == 1:
            return target_players[0].chips, True

        # 必要項目のリセット
        self.table.dealer.reset_round(self.players)

        # ディーラーボタンを動かす
        self.table.dealer.move_dealer_button(self.players)

        # プレイヤー情報の表示
        self.display_game_state()

        return target_players[0].chips, False
