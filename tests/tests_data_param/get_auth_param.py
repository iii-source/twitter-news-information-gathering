import os

"""
テストケースに対するテスト名を定義
"""
test_key = "valid"
test_key1 = "user_is_invalid"
test_key2 = "password_is_invalid"
test_key3 = "user_password_is_invalid"

"""
Basic認証用のuser passを取得する
"""


def get_test_auth():
    test = {'user': 'john', 'password': 'hello'}
    test_data = {
        test_key: test,
    }
    return test_data


def get_test_auth_admin():
    test = {'user': os.environ['ADMIN_USER'],
            'password': os.environ['ADMIN_PASSWORD']}
    test_data = {
        test_key: test,
    }
    return test_data


def get_test_auth03():
    test1 = {'user': 'foo', 'password': 'hello'}
    test2 = {'user': 'john', 'password': 'foo'}
    test3 = {'user': 'foo', 'password': 'foo'}
    test_data = {
        test_key1: test1,
        test_key2: test2,
        test_key3: test3,
    }
    return test_data
