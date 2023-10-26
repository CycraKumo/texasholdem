import json
import os


class DataManager:
    """データを管理するクラス。

    Attributes:
        data_file_path (str): データが保存されるファイルのパス。
        data (dict[str, obj]): ロードしたデータ。

    Tests:
        [ ]: test_data_manager

    """

    def __init__(self, file_path):
        """DataManagerクラスの初期化。

        Args:
            file_path (str): データが保存されるファイルのパス。

        Tests:
            [ ]:

        """
        self.data_file_path = file_path
        self.data = {}
        self.load_data()

    def load_data(self):
        """データをデータファイルから読み込む。

        Tests:
            [ ]:

        """
        if os.path.exists(self.data_file_path):
            with open(self.data_file_path, 'r') as file:
                self.data = json.load(file)
        else:
            self.data = {}

    def save_data(self):
        """データをデータファイルに保存する。

        Tests:
            [ ]:

        """
        with open(self.data_file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get_user_data(self, user_name):
        """指定されたデータを取得する。

        Args:
            user_name (str): データ名。

        Returns:
            obj: 取得したデータ。

        Tests:
            [ ]:

        """
        return self.data.get(user_name)

    def update_user_data(self, user_name, data):
        """指定されたデータを更新する。

        Args:
            user_name (str): データ名。
            data (obj): 更新するデータ。

        Tests:
            [ ]:

        """
        self.data[user_name] = data
        self.save_data()

    def add_new_user(self, user_name, initial_data):
        """新しいデータ名を追加し、初期データを設定する。

        Args:
            user_name (str): データ名。
            initial_data (obj): 初期データ。

        """
        if user_name not in self.data:
            self.data[user_name] = initial_data
            self.save_data()

    def delete_user(self, user_name):
        """指定されたデータ名を削除する。

        Args:
            user_name (str): データ名。

        """
        if user_name in self.data:
            del self.data[user_name]
            self.save_data()
