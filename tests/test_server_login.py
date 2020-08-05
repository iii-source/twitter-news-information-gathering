import os
import requests

# テスト対象のURLを定義
url = 'http://localhost:5000/login'


# 認証OKの場合
def test_server_login01():
    # リクエストAPI用jsonデータ作成
    payload = {'API_KEY': os.environ.get('API_KEY')}
    result = get_request(payload)
    assert result == 200


# 認証NGの場合
def test_server_login02():
    # リクエストAPI用jsonデータ作成
    payload = {'API_KEY': 'value_for_NG'}
    result = get_request(payload)
    assert result == 401


def get_request(payload):
    """
    getAPI用リクエスト

    Parameters
    ----------
    payload : dict
        リクエスト用データ

    Returns
    -------
    request_data : dict
        jsonパースしたResponseデータ
    """
    return requests.get(url, json=payload).json()


test_server_login01()
test_server_login02()
