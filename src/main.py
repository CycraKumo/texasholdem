import os

from data_manager import DataManager
from game import Game
from input_handler import InputHandler
from message_handler import MessageHandler


"""
[x]1.フィックスドリミット、ポットリミット、ノーリミットの実装
  [ ]1.1.ノーリミットの挙動確認
    [ ]1.1.1.ベットサイズの確認
    [ ]1.1.2.リファクタリング
  [ ]1.2.フィックスドリミットの実装
  [ ]1.3.ポットリミットの実装
[x]2.総チップ数の管理
[ ]3.ゲームモードの追加（リングゲーム、トーナメント）
[x]4.ゲームごとのチップの持ち込み
[ ]5.ゲーム中にプレイヤーのチップが0になった場合の処理
[ ]6.トーナメントにおいてはブラインドや賞金の設定
[ ]7.リングゲームにおいてはブラインドや席についているランダムCPUの数
[ ]8.AIの作成
  [ ]8.1.ちゃんとした設計

"""


class Main:
    """メインロジックのクラスです。

    ユーザーデータの読み込みやゲームロジックの実行を行います。

    Attributes:
        message_handler (MessageHandler): メッセージクラスのインスタンス。
        input_handler (InputHandler): ユーザー入力クラスのインスタンス。
        data_manager (DataManager): データマネージャークラスのインスタンス。

    Tests:
        [ ]: test_main

    """

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    USER_DATA_PATH = os.path.join(CURRENT_DIR, "..", "data", "user_data.json")

    def __init__(self):
        """コンストラクタ。

        """
        self.message_handler = MessageHandler()
        self.input_handler = InputHandler(self.message_handler)
        self.user_data_manager = DataManager(self.USER_DATA_PATH)

    def display_users_list(self):
        """プレイヤーの一覧を表示する。

        """
        self.user_data_manager.load_data()
        users_list = self.user_data_manager.data
        print(self.message_handler.get_message("user_list"))
        for user in users_list:
            print(user)

    def input_user_name(self):
        """ユーザーからの入力を受け付ける。

        """
        return input(self.message_handler.get_message("user_input"))

    def handle_user_data(self, user_name):
        """ユーザーデータの処理: 存在するかどうかを確認し、チップを取得または設定する。

        """
        users_list = self.user_data_manager.ata

        if user_name in users_list:
            print(self.message_handler.get_message("welcome_user", user_name=user_name))
            chips = self.user_data_manager.get_user_data(user_name)
            print(self.message_handler.get_message("now_chips", chips=chips))
        else:
            print(self.message_handler.get_message("add_user", user_name=user_name))
            initial_chips = 10000
            self.user_data_manager.add_new_user(user_name, initial_chips)
            print(self.message_handler.get_message("initial_chips", initial_chips=initial_chips))

    def start_game_flow(self):
        """ゲームをスタートする。

        """
        self.display_users_list()
        player_name = self.input_user_name()
        chips = self.user_data_manager.get_user_data(player_name)
        print(self.message_handler.get_message("now_chips", chips=chips))
        game_chips = self.input_handler.get_initial_chips()
        subtract_chips = chips - game_chips
        self.user_data_manager.update_user_data(player_name, subtract_chips)
        print(self.message_handler.get_message("now_chips", chips=subtract_chips))
        game = Game(self.message_handler, self.input_handler, player_name, game_chips)
        last_chips = game.start_game()
        add_chips = subtract_chips + last_chips
        self.user_data_manager.update_user_data(player_name, add_chips)
        print(self.message_handler.get_message("now_chips", chips=add_chips))


if __name__ == "__main__":

    main = Main()

    main.start_game_flow()
