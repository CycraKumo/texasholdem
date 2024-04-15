#!/usr/bin/python
# -*- coding: utf-8 -*-
"""モジュールの説明タイトル

* ソースコードの一番始めに記載すること
* importより前に記載する

Todo:
    TODOリストを記載
    * conf.pyの``sphinx.ext.todo`` を有効にしないと使用できない
    * conf.pyの``todo_include_todos = True``にしないと表示されない

"""


class testClass():
    """クラスの説明タイトル

    クラスについての説明文

    Attributes:
        属性の名前 (属性の型): 属性の説明
        属性の名前 (:obj:`属性の型`): 属性の説明.

    """

    def print_test(self, param1, param2):
        """関数の説明タイトル

        関数についての説明文

        Args:
            引数の名前 (引数の型): 引数の説明
            引数の名前 (:obj:`引数の型`, optional): 引数の説明.

        Returns:
            戻り値の型: 戻り値の説明 (例 : True なら成功, False なら失敗.)

        Raises:
            例外の名前: 例外の説明 (例 : 引数が指定されていない場合に発生 )

        Yields:
            戻り値の型: 戻り値についての説明

        Examples:

            関数の使い方について記載

            >>> print_test ("test", "message")
               test message

        Note:
            注意事項などを記載

        """
        print("%s %s" % (param1, param2))


if __name__ == '__main__':

    test_object = testClass()
    test_object.print_test("test", "message")
