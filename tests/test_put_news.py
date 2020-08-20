from tests import requests_operation as ro

URL_REF = 'https://iii-source.github.io/public/' \
          'swagger_ui/tweet_news/docs/dist/'


# 正常系 通常更新
def test_news01():
    # リクエストAPI用jsonデータ作成
    payload = {'description': 'description_test'}
    result = ro.put_request(get_url('3'), payload)
    assert result['message'] == 'Updated successfully.'
    assert result['code'] == 200


# 正常系 更新が正しく出来ているか確認
def test_news02():
    result = ro.get_request(get_url('3'))
    for record in result['records']:
        assert record['newsid'] == 3
        assert record['news_date'] == '2020-08-10'
        assert record['url'] == 'https://hogehoge3'
        assert record['description'] == 'description_test'


# 正常系 検索にヒットしなかった場合
def test_news03():
    # リクエストAPI用jsonデータ作成
    result = ro.get_request(get_url('99'))
    assert result['message'] == 'not found newsid'
    assert result['code'] == 404


# 異常系 不正なデータ型(数字型)
def test_news04():
    # リクエストAPI用jsonデータ作成
    result = ro.get_request(get_url('AAAAA'))
    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF


# 異常系 SQL インジェクション
def test_news05():
    # リクエストAPI用jsonデータ作成
    result = ro.get_request(get_url('10 or 1 = 1'))
    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF

    result = ro.get_request(get_url('0; 1 = 1'))
    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF

    result = ro.get_request(get_url('0; select * from news'))
    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF


def get_url(id):
    # テスト対象のURLを定義
    return 'http://localhost:5000/news/' + id
