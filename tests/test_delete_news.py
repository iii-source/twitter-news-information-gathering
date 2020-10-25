import pytest
from tests.tests_data_param import get_auth_param as td
from tests import requests_operation as ro

URL_REF = 'https://iii-source.github.io/public/' \
          'swagger_ui/tweet_news/docs/dist/'


# 有効期限内用uuid取得
@pytest.fixture()
@pytest.mark.parametrize("inputs_auth", list(td.get_test_auth_admin().values()),
                         ids=list(td.get_test_auth_admin().keys()))
def constant_uuid(inputs_auth):
    result = ro.get_request_with_auth(inputs_auth['user'], inputs_auth['password'])
    # tokenを取得
    return max(record['token'] for record in result['records'])


# TODO (scope="module")を指定するとエラーが発生するようになってしまう。
@pytest.fixture#(scope="module")
@pytest.mark.parametrize("inputs_auth", list(td.get_test_auth_admin().values()),
                         ids=list(td.get_test_auth_admin().keys()))
def constant_newsid(inputs_auth, constant_uuid):
    headers = {'X-Request-ID': constant_uuid}
    # インクリメント確認用
    result = ro.get_request(get_url(), headers)
    # listの中で一番価の高いnewsidを取得
    return max(record['newsid'] for record in result['records'])


# TODO constant_newsidをmoduleごとに呼び出すことが出来ないためテスト不可
# newsテーブル 最新のnewsidを取得
# @pytest.mark.parametrize("inputs", list(td.get_test_auth_admin().values()),
#                          ids=list(td.get_test_auth_admin().keys()))
# def test_advance_preparation(inputs, constant_newsid):
#     # こちら事前に呼び出しておくことで更新前newsid最大値を事前に取得し固定
#     pass


# 正常系 通常取得
@pytest.mark.parametrize("inputs_auth", list(td.get_test_auth_admin().values()),
                         ids=list(td.get_test_auth_admin().keys()))
def test_news01(inputs_auth, constant_uuid, constant_newsid):
    headers = {'X-Request-ID': constant_uuid}
    # リクエストAPI用jsonデータ作成
    result = ro.delete_request(get_url_with_id(constant_newsid), headers)
    assert result['message'] == 'Deleted successfully.'
    assert result['code'] == 200


# TODO constant_newsidをmoduleごとに呼び出すことが出来ないためテスト不可
# 正常系 検索にヒットしなかった場合(先ほど削除したnewsidを検索し正しく削除されているか)
# @pytest.mark.parametrize("inputs", list(td.get_test_auth_admin().values()),
#                          ids=list(td.get_test_auth_admin().keys()))
# def test_news02(inputs, constant_uuid, constant_newsid):
#     headers = {'X-Request-ID': constant_uuid}
#     # リクエストAPI用jsonデータ作成
#     result = ro.delete_request(get_url_with_id(constant_newsid), headers)
#     assert result['message'] == 'not found newsid'
#     assert result['code'] == 404


# 準正常系 不正なデータ型(文字列)
@pytest.mark.parametrize("inputs_auth", list(td.get_test_auth_admin().values()),
                         ids=list(td.get_test_auth_admin().keys()))
def test_news03(inputs_auth, constant_uuid):
    headers = {'X-Request-ID': constant_uuid}
    # リクエストAPI用jsonデータ作成
    result = ro.delete_request(get_url_with_id('AAAAA'), headers)
    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF


# 準正常系 SQL インジェクション
@pytest.mark.parametrize("inputs_auth", list(td.get_test_auth_admin().values()),
                         ids=list(td.get_test_auth_admin().keys()))
def test_news04(inputs_auth, constant_uuid):
    headers = {'X-Request-ID': constant_uuid}
    # リクエストAPI用jsonデータ作成
    result = ro.delete_request(get_url_with_id('10 or 1 = 1'), headers)
    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF

    result = ro.delete_request(get_url_with_id('0; 1 = 1'), headers)
    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF


def get_url_with_id(id):
    # テスト対象のURLを定義
    return 'http://localhost:5000/news/' + str(id)


def get_url():
    # テスト対象のURLを定義
    return 'http://localhost:5000/news/'
