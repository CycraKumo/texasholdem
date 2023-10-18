import random

from dealer import Dealer
from input_handler import InputHandler
from message_handler import MessageHandler
from player import Player


class Game:
    """
    Texas Hold'em Poker Gameのメインロジックを管理するクラス。
    """

    def __init__(self):
        """
        Gameクラスのインスタンスを初期化する。
        必要なインスタンス変数の初期化や他のクラスのインスタンス化を行う。
        """
        self.message_handler = MessageHandler()
        self.input_handler = InputHandler(self.message_handler)
        self.dealer = Dealer(self.message_handler, self.input_handler)

    def start_game(self):
        """
        ゲームを開始する。
        ゲームの開始時の前処理とメイン処理を順に実行する。
        """
        self.pre_process()
        while True:
            self.main_process()

    def pre_process(self):
        """
        ゲーム開始前の処理を行う。
        例: プレイヤーの登録、初期配置のセットアップなど
        """
        # プレイヤー名の入力
        player_name = self.input_handler.get_player_name()

        # 初期チップの入力
        initial_chips = self.input_handler.get_initial_chips()

        # CPUの人数の入力
        num_cpu = self.input_handler.get_num_cpu()

        # プレイヤーインスタンスの生成
        self.players = [Player(name=player_name, chips=initial_chips, input_handler=self.input_handler)]
        for i in range(num_cpu):
            self.players.append(Player(name=f"CPU{i+1}", chips=initial_chips, input_handler=self.input_handler, is_cpu=True))

        # ランダムに席につかせる
        random.shuffle(self.players)

        # ディーラーボタン配置の決定
        print(self.message_handler.get_message("set_initial_button"))
        self.input_handler.wait_for_user()
        button_holder = self.dealer.set_initial_button(self.players)
        print(self.message_handler.get_message("button_holder", player_name=button_holder.name))
        self.input_handler.wait_for_user()

        # プレイヤー情報の表示
        self.display_game_state()

    def collect_blinds(self):
        """
        Small BlindとBig Blindを徴収します。
        """
        # ボタンの位置を取得
        dealer_position = next(i for i, player in enumerate(self.players) if player.is_dealer)
        # SBとBBの位置を計算
        sb_position = (dealer_position + 1) % len(self.players)
        bb_position = (dealer_position + 2) % len(self.players)

        # SBとBBのプレイヤーを取得
        sb_player = self.players[sb_position]
        bb_player = self.players[bb_position]

        self.sb_amount = 1  # ここは任意のSBの額を設定できます。
        self.bb_amount = 2  # ここは任意のBBの額を設定できます。

        # SBとBBの徴収
        sb_player.bet(self.sb_amount)
        bb_player.bet(self.bb_amount)

        # プレイヤー情報の表示
        self.display_game_state()

    def display_game_state(self):
        """
        ゲームの現在の状態を表示します（プレイヤー情報、コミュニティカードなど）。
        """
        # コミュニティカードの情報
        self.message_handler.display_community_cards(self.dealer.community_cards, sum(pot.total for pot in self.dealer.pots))

        # プレイヤー情報
        print(self.message_handler.display_players_info(self.players))

        # ユーザーからの入力待機
        self.input_handler.wait_for_user()

    def main_process(self):
        """
        ゲームのメインロジックを実行する。
        プリフロップ、フロップ、ターン、リバーなどの各段階での処理を行う。
        """
        # デッキの作り直し
        self.dealer.deck.generate_deck()

        # SBとBBの徴収
        self.collect_blinds()

        # 各プレイヤーに２枚ずつカードを配る
        self.dealer.deal_hole_cards(self.players)

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
        remaining_players = self.dealer.bet_round(self.players, "pre_flop", self.bb_amount)

        # 賭け金をポットに移動。その他bet_round関数で設定した値の初期化処理
        self.dealer.pot_collect(self.players)

        # プレイヤー情報の表示
        self.display_game_state()

        if len(remaining_players) > 1:

            for key, num_cards in community_cards_dict.items():

                # コミュニティカードをめくる
                self.dealer.reveal_community_cards(num_cards)

                # プレイヤー情報の表示
                self.display_game_state()

                # フロップ、ターン、リバーベッティングラウンドを開始
                remaining_players = self.dealer.bet_round(self.players, key)

                # 賭け金をポットに移動。その他bet_round関数で設定した値の初期化処理
                self.dealer.pot_collect(self.players)

                # プレイヤー情報の表示
                self.display_game_state()

                if len(remaining_players) == 1:
                    break

        # ここまででlen(remaining_players)が2以上なら、アクティブなプレイヤーで手の強さ比べを行う
        if len(remaining_players) > 1:
            self.dealer.evaluate_and_fold_players(remaining_players)
        else:
            self.dealer.distribute_pot(remaining_players)

        # ユーザーからの入力待機
        self.input_handler.wait_for_user()

        # 必要項目のリセット
        self.dealer.reset_round(self.players)

        # ディーラーボタンを動かす
        self.dealer.move_dealer_button(self.players)

        # プレイヤー情報の表示
        self.display_game_state()
