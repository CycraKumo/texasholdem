from data_manager import DataManager
from game_lobby import GameLobby
from input_handler import InputHandler
from message_handler import MessageHandler


"""
[ ]0.ちゃんとした設計
    [x]0.1.システムアーキテクチャ図
    [x]0.2.クラス図
    [ ]0.3.シーケンス図
    [ ]0.4.データフロー図
    [-]0.5.ER図
    [ ]0.6.ユースケース図
    [ ]0.7.アクティビティ図
    [ ]0.8.ステート図
[x]1.フィックスドリミット、ポットリミット、ノーリミットの実装
    [x]1.1.ノーリミットの挙動確認
        [x]1.1.1.ベットサイズの確認
    [x]1.2.フィックスドリミットの実装
[x]2.総チップ数の管理
    [x]2.1.user_data.jsonへのCRUD
    [x]2.2.テーブル選択時に、今持っているチップの表示
    [x]2.3.テーブルへの持ち込み時の減算
    [x]2.4.ゲーム終了時の加算
[ ]3.ゲームモードの追加（リングゲーム、トーナメント）
    [ ]3.1.BBの額によるテーブルの追加（まずはリングゲームから）
        [ ]3.1.1.ゲームの途中でCPUを追加
        [ ]3.1.2.ゲームの途中で席を立つシステム
    [ ]3.2.トーナメントの追加
        [ ]3.2.1.1テーブルトーナメントの実装
        [ ]3.2.2.複数テーブルトーナメントの実装
[x]4.ゲーム中にチップが0になった場合の処理
    [ ]4.1.ゲーム中にプレイヤーのチップが0になった場合の処理
        [ ]4.1.1.チップのリバイ
        [x]4.1.2.席を立つ
    [x]4.2.ゲーム中にCPUのチップが0になった場合の処理（3.1.1、3.2につながる）
        [x]4.2.1.チップのリバイ
        [x]4.2.2.席を立つ
[ ]5.トーナメントにおけるブラインドや賞金の設定
[ ]6.全体的なリファクタリング
[ ]7.AIの作成
    [ ]7.1.ちゃんとした設計

"""

# ↓ここがメインの処理
if __name__ == "__main__":
    try:
        # 初期値の定義
        player_name, last_chips = None, None

        # クラスのインスタンス化
        message_handler = MessageHandler()
        input_handler = InputHandler(message_handler)
        data_manager = DataManager("./data/user_data.json")

        # プレイヤー名の取得、プレイヤー名に紐づくセーブデータの取得
        player_name = input_handler.get_player_name()
        last_chips = data_manager.get_or_create_user_data(player_name)

        # ゲームロビーのインスタンス化
        game_lobby = GameLobby(message_handler, input_handler, data_manager, player_name)

        # ゲームのメインループ
        while True:
            # テーブル一覧の表示
            game_lobby.display_tables()

            # ゲームの開始
            last_chips, end_flg = game_lobby.start_game()

            # ゲームの終了
            if end_flg:
                break

    # プログラム終了時に、プレイヤー名と最後のチップ数を保存
    finally:
        if player_name is not None and last_chips is not None:
            data_manager.update_user_data(player_name, last_chips)
