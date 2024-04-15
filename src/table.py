from dealer import Dealer


class Table:
    """テーブルを管理するクラス

    Attributes:



    Tests:
        [ ]: test_table

    """

    def __init__(self, message_handler, input_handler):
        """Tableクラスのインスタンスを初期化する。

        必要なインスタンス変数の初期化や他のクラスのインスタンス化を行う。

        Args:
            message_handler (MessageHandler): メッセージ処理のインスタンス。
            input_handler (InputHandler): 入力処理のインスタンス。

        """
        self.message_handler = message_handler
        self.input_handler = input_handler
        self.dealer = Dealer(self.message_handler, self.input_handler)
