import pytest
from tests.tests_data_param import get_auth_param as td
from tests import requests_operation as ro

URL_REF = 'https://iii-source.github.io/public/' \
          'swagger_ui/tweet_news/docs/dist/'


# 有効期限内用uuid取得
@pytest.fixture()
@pytest.mark.parametrize("inputs", list(td.get_test_auth().values()),
                         ids=list(td.get_test_auth().keys()))
def constant_uuid(inputs):
    result = ro.get_request_with_auth(inputs['user'], inputs['password'])
    # tokenを取得
    return max(record['token'] for record in result['records'])


# 正常系 通常取得
@pytest.mark.parametrize("inputs", list(td.get_test_auth().values()),
                         ids=list(td.get_test_auth().keys()))
def test_news_all01(inputs, constant_uuid):
    headers = {'X-Request-ID': constant_uuid}
    # リクエストAPI用jsonデータ作成
    result = ro.get_request(get_url(), headers)
    for i, record in enumerate(result['records']):
        if i == 0:
            assert record['newsid'] == 1
            assert record['news_date'] == '2020-08-07'
            assert record['url'] == 'https://hogehoge1'
            assert record['description'] == '説明を日本語で記す'
        elif i == 1:
                assert record['newsid'] == 2
                assert record['news_date'] == '2020-08-09'
                assert record['url'] == 'https://hogehoge2'
                assert record['description'] == 'english discription1'
        else:
            break


def get_url():
    # テスト対象のURLを定義
    return 'http://localhost:5000/news/'
