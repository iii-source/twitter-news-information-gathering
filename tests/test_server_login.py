import os
import requests


# 認証OKの場合
def test_server_login01():
    # リクエストAPI用jsonデータ作成
    payload = {'API_KEY': os.environ.get('API_KEY')}
    result = get_request(get_login_url(), payload)
    assert result == 200


# 認証NGの場合
def test_server_login02():
    # リクエストAPI用jsonデータ作成
    payload = {'API_KEY': 'value_for_NG'}
    result = get_request(get_login_url(), payload)
    assert result == 401


def get_login_url():
    # テスト対象のURLを定義
    return 'http://localhost:5000/user/login'


def get_request(url, payload):
    """
    getAPI用リクエスト

    Parameters
    ----------
    url : string
        リクエスト用url
    payload : dict
        リクエスト用データ

    Returns
    -------
    request_data : dict
        jsonパースしたResponseデータ
    """
    return requests.get(url, json=payload).json()
