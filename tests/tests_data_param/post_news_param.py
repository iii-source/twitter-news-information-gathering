"""
テストケースに対するテスト名を定義
"""
test_key = "valid"
test_key1 = "news_date_is_invalid"
test_key2 = "url_is_invalid"
test_key3 = "description_is_invalid"

"""
payload作成用のパラメーターを定義し取得できる関数をテストケースごとに配置
"""


def get_test_news_post01():
    test1 = ('2020-08-14', 'https://post-test', 'pytest_' + __name__)
    test_data = {
        test_key: test1
    }
    return test_data


def get_test_news_post05():
    test1 = (99, "https://hooooo", 'pytest_' + __name__)
    test2 = ("2020-08-20", 99, 'pytest_' + __name__)
    test3 = ("2020-08-20", "https://hooooo", 99)
    test_data = {
        test_key1: test1,
        test_key2: test2,
        test_key3: test3
    }
    return test_data


def get_test_news_post06():
    test1 = (None, "https://hooooo", 'pytest_' + __name__)
    test2 = ("2020-08-20", None, 'pytest_' + __name__)
    test3 = ("2020-08-20", "https://hooooo", None)
    test_data = {
        test_key1: test1,
        test_key2: test2,
        test_key3: test3
    }
    return test_data


class PostNews:
    """
    渡されたdictを元にpayloadを作成し保持する。

    Attributes
    ----------
    kwargs : dict
        payload作成用のdict
    """
    def __init__(self, **kwargs):
        self.payload = kwargs

    def get_news_param(self):
        return self.payload
