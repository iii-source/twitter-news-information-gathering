from common.response_message.error_response import error_response_400
from tests import requests_operation as ro
from tests.tests_data_param import post_news_param as td
import pytest

URL_REF = 'https://iii-source.github.io/public/' \
          'swagger_ui/tweet_news/docs/dist/'


# TODO 1 テストケースごとにパラメータを取得
# TODO 2 1で取得したパラメータをset_post_newsに渡しpayload作成
# TODO 3 12の処理をテストケース開始前にfixtureで事前に作成可能にすること
# 1テストケースごとに呼ばれる 引数に渡した数だけインスタンスが生成される
def set_post_news(inputs):
    # [0]: news_date, [1]: url, [2]: title, [3]: description
    return td.PostNews(news_date=inputs[0], url=inputs[1],
                       title=inputs[2], description=inputs[3])


# inputsによって作成するdictionaryを動的に作成可能にする。
def set_post_news01(inputs):
    # [0]: news_date, [1]: url, [2]: title, [3]: description
    # 各パラメーター必須チェック
    if inputs[0] is None:
        # news_date None
        return td.PostNews(url=inputs[1], title=inputs[2], description=inputs[3])
    elif inputs[1] is None:
        # url None
        return td.PostNews(news_date=inputs[0], title=inputs[2], description=inputs[3])
    elif inputs[2] is None:
        # title None
        return td.PostNews(news_date=inputs[0], url=inputs[1], description=inputs[3])
    elif inputs[3] is None:
        # description None
        return td.PostNews(news_date=inputs[0], url=inputs[1], title=inputs[2])



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
    # dict_valueをlistに加工
    insert = list(td.get_test_news_post01().values())
    # listをアンパックしpayloadのパラメーターを取得
    insert_param = insert[0]
    # payload用インスタンス作成
    po = set_post_news(insert_param)
    # 作成したpayloadを取得
    payload = po.get_news_param()
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

    # dict_valueをlistに加工
    insert = list(td.get_test_news_post01().values())
    # listをアンパックしpayloadのパラメーターを取得
    insert_param = insert[0]
    # payload用インスタンス作成
    po = set_post_news(insert_param)
    # 作成したpayloadを取得
    payload = po.get_news_param()
    # reversed(result['records'] = 最新レコードのみで判定を行う
    # = 今回追加したレコード(test_news_post01で使用したパラメータ)のみ判定を行う
    for record in reversed(result['records']):
        assert record['newsid'] == before_update_newsid
        assert record['news_date'] == payload['news_date']
        assert record['url'] == payload['url']
        assert record['title'] == payload['title']
        assert record['description'] == payload['description']
        break


#  TODO 期待値データ 判定予定 中身を1つ1つ精査するのではなく全てひと塊で判定する
error_response_400


# 異常系 不正なデータ型(API bodyのデータ型が仕様と異なる場合)
@pytest.mark.parametrize("inputs", list(td.get_test_news_post05().values()),
                         ids=list(td.get_test_news_post05().keys()))
def test_news_post05(inputs):
    # ※下記でも実施可能だが可読性を考慮し別パターンで実装
    # PostNewsインスタンスを作成しbad_newsインスタンス変数を取得(不正データ実行用payload取得)
    # payload = set_post_news(inputs).__dict__.get('payload')

    # payload用インスタンス作成
    po = set_post_news(inputs)
    # 作成したpayloadを取得
    payload = po.get_news_param()
    # 不正データ実行
    result = ro.post_request(get_url(), payload)
    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF


# 異常系 不正なkey(API bodyのデータの必須keyがない場合)
@pytest.mark.parametrize("inputs", list(td.get_test_news_post06().values()),
                         ids=list(td.get_test_news_post06().keys()))
def test_news_post06(inputs):
    # payload用インスタンス作成
    po = set_post_news01(inputs)
    # 作成したpayloadを取得
    payload = po.get_news_param()
    result = ro.post_request(get_url(), payload)

    assert result['message'] == 'Bad Request'
    assert result['errors']['code'] == 400
    assert result['errors']['url_ref'] == URL_REF


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
