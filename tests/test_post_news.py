from tests import requests_operation as ro
import pytest

URL_REF = 'https://iii-source.github.io/public/' \
          'swagger_ui/tweet_news/docs/dist/'


# 全テストで使用予定
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


# 正常系 通常挿入
def test_news_post01():
    # リクエストAPI用jsonデータ作成
    payload = {
        'news_date': '2020-08-14',
        'url': 'https://post-test',
        'description': 'description_test_from_pytest'
    }
    result = ro.post_request(get_url(), payload)
    assert result['message'] == 'Inserted successfully.'
    assert result['code'] == 200


# TODO 後処理でSERIALをリセットしないと失敗するため改善予定
# 正しくインクリメントされているか確認
def test_news_post02(constant_newsid):
    # 全レコード取得
    result = ro.get_request(get_url())
    # 挿入前最新newsid + 1 = 新しく挿入されたnewsid
    expected_1 = int(constant_newsid) + 1
    # 全レコード内から最新newsidを取得
    actual = max(record['newsid'] for record in result['records'])
    # 挿入前最新newsid + 1 == 新しく挿入されたnewsid
    assert expected_1 == actual


# 正常系 挿入が正しく出来ているか確認
def test_news_post03(constant_newsid):
    # 全レコードを取得
    result = ro.get_request(get_url())
    # 挿入前最新newsid + 1
    before_update_newsid = int(constant_newsid) + 1
    # reversed(result['records'] = 最新レコードのみで判定を行う
    # = 今回追加したレコードのみ判定を行う
    for record in reversed(result['records']):
        assert record['newsid'] == before_update_newsid
        assert record['news_date'] == '2020-08-14'
        assert record['url'] == 'https://post-test'
        assert record['description'] == 'description_test_from_pytest'
        break


# # TODO 事後処理 テストデータ整理  fixture
# def post_process():
#     pass
# SELECT * FROM news_newsid_seq;
# delete from news where newsid >= 5;
# select setval ('news_newsid_seq', 4);
# SELECT * FROM news_newsid_seq;

def get_url():
    # テスト対象のURLを定義
    return 'http://localhost:5000/news/'
