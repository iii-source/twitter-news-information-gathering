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


# 正常系 通常更新
@pytest.mark.parametrize("inputs", list(td.get_test_auth().values()),
                         ids=list(td.get_test_auth().keys()))
def test_news01(inputs, constant_uuid):
    headers = {'X-Request-ID': constant_uuid}
    # リクエストAPI用jsonデータ作成
    payload = {'description': 'description_test'}
    result = ro.put_request(get_url('3'), payload, headers)
    assert result['message'] == 'Updated successfully.'
    assert result['code'] == 200


# 正常系 更新が正しく出来ているか確認
@pytest.mark.parametrize("inputs", list(td.get_test_auth().values()),
                         ids=list(td.get_test_auth().keys()))
def test_news02(inputs, constant_uuid):
    headers = {'X-Request-ID': constant_uuid}
    result = ro.get_request(get_url('3'), headers)
    for record in result['records']:
        assert record['newsid'] == 3
        assert record['news_date'] == '2020-08-10'
        assert record['url'] == 'https://hogehoge3'
        assert record['description'] == 'description_test'


# 正常系 検索にヒットしなかった場合
@pytest.mark.parametrize("inputs", list(td.get_test_auth().values()),
                         ids=list(td.get_test_auth().keys()))
def test_news03(inputs, constant_uuid):
    headers = {'X-Request-ID': constant_uuid}
    # リクエストAPI用jsonデータ作成
    result = ro.get_request(get_url('99'), headers)
    assert result['message'] == 'not found newsid'
    assert result['code'] == 404


# 準正常系 不正なデータ型(数字型)
@pytest.mark.parametrize("inputs", list(td.get_test_auth().values()),
                         ids=list(td.get_test_auth().keys()))
def test_news04(inputs, constant_uuid):
    headers = {'X-Request-ID': constant_uuid}
    # リクエストAPI用jsonデータ作成
    result = ro.get_request(get_url('AAAAA'), headers)
    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF


# 準正常系 SQL インジェクション
@pytest.mark.parametrize("inputs", list(td.get_test_auth().values()),
                         ids=list(td.get_test_auth().keys()))
def test_news05(inputs, constant_uuid):
    headers = {'X-Request-ID': constant_uuid}
    # リクエストAPI用jsonデータ作成
    result = ro.get_request(get_url('10 or 1 = 1'), headers)
    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF

    result = ro.get_request(get_url('0; 1 = 1'), headers)
    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF

    result = ro.get_request(get_url('0; select * from news'), headers)
    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF


def get_url(id):
    # テスト対象のURLを定義
    return 'http://localhost:5000/news/' + id
