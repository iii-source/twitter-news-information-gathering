import os
from flask import Flask, request
# from .information_gathering import tweet_main
from app import sql_id_yaml
from app import AuthorizationUuid
from common.db import Database as Database
from common.response_message import response, error_response
from common.validate.validate import validate_schema
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()


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
    return postgres_instance.select(
        sql_id_yaml['select_get_news'],
        newsid
    )


# TODO デコレーターからデコレーター呼び出し validate_schema(validate_json)
@app.route('/news/<newsid>', methods=["PUT"])
@validate_schema
def put_news(newsid):
    return postgres_instance.update(
        sql_id_yaml['put_news'],
        request.get_json()['description'],
        newsid
    )


@app.route('/news/<newsid>', methods=["DELETE"])
def delete_news(newsid):
    return postgres_instance.delete(
        sql_id_yaml['delete_news'],
        newsid
    )


@app.route('/news/', methods=["GET"])
def news_all():
    return postgres_instance.select(
        sql_id_yaml['select_get_news_all']
    )


@app.route('/news/', methods=["POST"])
@validate_schema
def post_news():
    return postgres_instance.insert(
        sql_id_yaml['post_news'],
        list(request.get_json().values())
    )

# # TODO メイン処理呼び出し
# @app.route('/tweet_main', methods=["GET", "POST"])
# def main():
#     tweet_main()


if __name__ == '__main__':
    postgres_instance = Database.Database()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
