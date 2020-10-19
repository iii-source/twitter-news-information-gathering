import os
import requests
import pprint
from flask import Flask, request
from app import information_gathering as info_gathe
from app import sql_id_yaml
from app import AuthorizationUuid
from common.authentication.authentication import check_headers_uuid
from common.db import Database as Database
from common.response_message import response, error_response
from common.validate.validate import validate_schema
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()
# 一般ユーザー用権限
LEVEL0 = 0
# 管理者ユーザー用権限
LEVEL1 = 1


@app.route('/user/login', methods=["GET"])
@auth.login_required
def login():
    # _get_authentication実施し、認証OK後の処理
    auth_uuid = AuthorizationUuid.AuthorizationUuid(postgres_instance, auth)
    return auth_uuid.users_login()


@auth.get_password
def __get_authentication(username):
    # DBにあるuser passを取得
    get_results = postgres_instance.select(
        sql_id_yaml['select_get_users_all']
    )
    # APIのuser pass とDBのuser passを照合
    for get_result in get_results['records']:
        if username == get_result['user_name']:
            # APIと一致するDBの値で認証される
            return get_result['password']
    # 一致しなかった場合はUnauthorized Accessが返される(Noneで認証判定されNGが出る)
    return None


@app.route('/news/<newsid>', methods=["GET"])
def news(newsid):
    # uuidのチェック
    result = check_headers_uuid(postgres_instance)
    try:
        if result['records'][0]['access_level'] == LEVEL0 or LEVEL1:
            # 正常応答だった場合
            return postgres_instance.select(
                sql_id_yaml['select_get_news'],
                newsid
            )
        else:
            # X-Request-IDが一致していない or 有効期限外だった場合
            return result
    except KeyError as e:
        # X-Request-IDが一致していない or 有効期限外だった場合
        return result


# TODO デコレーターからデコレーター呼び出し validate_schema(validate_json)
@app.route('/news/<newsid>', methods=["PUT"])
@validate_schema
def put_news(newsid):
    # uuidのチェック
    result = check_headers_uuid(postgres_instance)
    try:
        if result['records'][0]['access_level'] == LEVEL0 or LEVEL1:
            # 正常応答だった場合
            return postgres_instance.update(
                sql_id_yaml['put_news'],
                *list(request.get_json().values()),
                where_id=newsid
            )
        else:
            # X-Request-IDが一致していない or 有効期限外だった場合
            return result
    except KeyError as e:
        # X-Request-IDが一致していない or 有効期限外だった場合
        return result


@app.route('/news/<newsid>', methods=["DELETE"])
def delete_news(newsid):
    # 特殊認証チェック
    result = check_headers_uuid(postgres_instance)
    try:
        if result['records'][0]['access_level'] == LEVEL1:
            # 正常応答だった場合
            return postgres_instance.delete(
                sql_id_yaml['delete_news'],
                newsid
            )
        else:
            # 1ではない = アクセス権限がないためエラー
            return error_response.error_response_403()
    except KeyError as e:
        # X-Request-IDが一致していない or 有効期限外だった場合
        return error_response.error_response_403_expired_or_incorrect_uuid()


@app.route('/news/', methods=["GET"])
def news_all():
    # uuidのチェック
    result = check_headers_uuid(postgres_instance)
    try:
        if result['records'][0]['access_level'] == LEVEL0 or LEVEL1:
            # 正常応答だった場合
            return postgres_instance.select(
                sql_id_yaml['select_get_news_all']
            )
        else:
            # X-Request-IDが一致していない or 有効期限外だった場合
            return result
    except KeyError as e:
        # X-Request-IDが一致していない or 有効期限外だった場合
        return result


@app.route('/news/', methods=["POST"])
@validate_schema
def post_news():
    # 特殊認証チェック
    result = check_headers_uuid(postgres_instance)
    try:
        if result['records'][0]['access_level'] == LEVEL1:
            # 正常応答だった場合
            return postgres_instance.insert(
                sql_id_yaml['post_news'],
                list(request.get_json().values())
            )
        else:
            # 1ではない = アクセス権限がないためエラー
            return error_response.error_response_403()
    except KeyError as e:
        # X-Request-IDが一致していない or 有効期限外だった場合
        return error_response.error_response_403_expired_or_incorrect_uuid()


# TODO ここら辺全般の処理を外出ししたい デコレーターを使用してチェックしたい(ここに書きたくない)
@app.route('/tweet_main', methods=["GET", "POST"])
@auth.login_required
def main():
    # Basic認証(管理者ユーザー) uuidを更新
    auth_uuid = AuthorizationUuid.AuthorizationUuid(postgres_instance, auth)
    result_login_data = auth_uuid.users_login()

    # DB格納用データ twitterより取得
    result_list = info_gathe.tweet_main()

    # headerに取得したuuidを付与しAPI実行
    headers = {'X-Request-ID': result_login_data['records'][0]['token']}

    # DBへ格納可能か判定用既存データ取得
    news_list = requests.get('http://localhost:5000/news/', headers=headers).json()
    pprint.pprint(news_list)
    # DBに新規登録するnews情報のリスト
    register_news_list = []
    # 存在判定用リスト
    url_list = []

    # news_list: 現在DBにあるnews一覧
    for news in news_list['records']:
        url_list.append(news['url'])

    # result_list: 現在twitterから取得してきたnews一覧
    for result in result_list:
        # twitterAPIで取得したnewのurlが現在DBにあるurlと一致していない(新規news)
        if result['url'] not in url_list:
            # 現在のDBに存在しないurlの場合登録
            register_news_list.append(result)

    pprint.pprint(register_news_list)

    # 取得したjsonデータをnewsテーブルに格納 post_newsを呼び出す。
    for register_news in register_news_list:
        requests.post('http://localhost:5000/news/', headers=headers, json=register_news).json()
    return response.response_200_tweet_main()


if __name__ == '__main__':
    postgres_instance = Database.Database()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
