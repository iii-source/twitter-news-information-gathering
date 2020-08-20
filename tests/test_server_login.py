import os
from tests import requests_operation as ro


# 認証OKの場合
def test_server_login01():
    # リクエストAPI用jsonデータ作成
    payload = {'API_KEY': os.environ.get('API_KEY')}
    result = ro.get_request_with_body(get_url(), payload)
    assert result['message'] == 'accepted the certificate.'
    assert result['code'] == 200


# 認証NGの場合
def test_server_login02():
    # リクエストAPI用jsonデータ作成
    payload = {'API_KEY': 'value_for_NG'}
    result = ro.get_request_with_body(get_url(), payload)
    assert result['message'] == 'certification failed.'
    assert result['code'] == 401


def get_url():
    # テスト対象のURLを定義
    return 'http://localhost:5000/user/login'
