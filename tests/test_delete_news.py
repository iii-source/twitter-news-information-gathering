from tests import requests_operation as ro
import pytest

URL_REF = 'https://iii-source.github.io/public/' \
          'swagger_ui/tweet_news/docs/dist/'


@pytest.fixture(scope="module")
def constant_newsid():
    # インクリメント確認用
    result = ro.get_request(get_url())
    # listの中で一番価の高いnewsidを取得
    return max(record['newsid'] for record in result['records'])


# newsテーブル 最新のnewsidを取得
def test_advance_preparation(constant_newsid):
    # こちら事前に呼び出しておくことで更新前newsid最大値を事前に取得し固定
    pass


# 正常系 通常取得
def test_news01(constant_newsid):
    # リクエストAPI用jsonデータ作成
    result = ro.delete_request(get_url_with_id(constant_newsid))
    assert result['message'] == 'Deleted successfully.'
    assert result['code'] == 200


# 正常系 検索にヒットしなかった場合(先ほど削除したnewsidを検索し正しく削除されているか)
def test_news02(constant_newsid):
    # リクエストAPI用jsonデータ作成
    result = ro.delete_request(get_url_with_id(constant_newsid))
    assert result['message'] == 'not found newsid'
    assert result['code'] == 404


# 異常系 不正なデータ型(文字列)
def test_news03():
    # リクエストAPI用jsonデータ作成
    result = ro.delete_request(get_url_with_id('AAAAA'))
    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF


# 異常系 SQL インジェクション
def test_news04():
    # リクエストAPI用jsonデータ作成
    result = ro.delete_request(get_url_with_id('10 or 1 = 1'))
    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF

    result = ro.delete_request(get_url_with_id('0; 1 = 1'))
    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF


def get_url_with_id(id):
    # テスト対象のURLを定義
    return 'http://localhost:5000/news/' + str(id)


def get_url():
    # テスト対象のURLを定義
    return 'http://localhost:5000/news/'
