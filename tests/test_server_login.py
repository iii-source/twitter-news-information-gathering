from app import server_login as app


def test_server_login01():
    # TODO リクエストAPI用jsonデータ作成
    request_dict = {}
    # TODO status code 200 返却されればOK
    # TODO jsonパラメーター渡す
    assert app.server_login(request_dict) == 200


test_server_login01()
