from tests import requests_operation as ro
from tests.tests_data_param import get_auth_param as td
import pytest

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


# 正常系 有効期限内の場合
@pytest.mark.parametrize("inputs", list(td.get_test_auth().values()),
                         ids=list(td.get_test_auth().keys()))
def test_user_login01(inputs, constant_uuid):
    # リクエストAPI用jsonデータ作成
    result = ro.get_request_with_auth(inputs['user'], inputs['password'])

    # fixtureでは事前にuuidを払い出してもらう(固定)
    # actual fixtureで事前に用意したuuid
    # expect 今回新たに取得したuuid
    # actual expect は同じになるはず
    for record in result['records']:
        assert record['token'] == constant_uuid


# TODO 有効期限切れuuidを事前に取得し更新後uuidと比較できるようにする。
# 正常系 有効期限切れの場合
# @pytest.mark.parametrize("inputs", list(td.get_test_auth().values()),
#                          ids=list(td.get_test_auth().keys()))
# def test_user_login02(inputs, constant_uuid):
#     # リクエストAPI用jsonデータ作成
#     result = ro.get_request_with_auth(get_url(), inputs['user'], inputs['password'])
#     # fixtureでは事前にuuidを払い出してもらう(固定)
#     # actual fixtureで事前に用意したuuid
#     # expect 今回新たに取得したuuid
#     # actual expect は同じにならない uuidは更新されているので。
#
#     for record in result['records']:
#         assert record['token'] != constant_uuid


# 異常系 1: userが不一致, 2: passwordが不一致, 3: user passwordが不一致
@pytest.mark.parametrize("inputs", list(td.get_test_auth03().values()),
                         ids=list(td.get_test_auth03().keys()))
def test_user_login03(inputs):
    # リクエストAPI用jsonデータ作成
    result = ro.get_request_with_auth(inputs['user'], inputs['password'])
    assert result.status_code == 401
