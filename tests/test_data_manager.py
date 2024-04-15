from data_manager import DataManager


def test_data_manager_initialization():
    """
    DataManagerクラスの初期化をテストします。

    Tests:

    """
    file_path = "./data/user_data.json"
    data_manager = DataManager(file_path)
    print(data_manager)
