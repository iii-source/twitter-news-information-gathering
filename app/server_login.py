import os
from flask import Flask, request
# from .information_gathering import tweet_main
from app import sql_id_yaml
from common.db import Database as Database
from common.response_message import response, error_response

app = Flask(__name__)


@app.route('/user/login', methods=["GET"])
def login():
    if request.get_json()['API_KEY'] == os.environ.get('API_KEY'):
        # # 認証OKの場合
        return response.response_200()
    else:
        # 認証NGの場合
        return response.response_401()


@app.route('/news/<newsid>', methods=["GET"])
def news(newsid):
    return postgres_instance.select(
        sql_id_yaml['select_get_news'],
        newsid
    )


@app.route('/news/', methods=["GET"])
def news_all():
    return postgres_instance.select(
        sql_id_yaml['select_get_news_all']
    )


# # TODO メイン処理呼び出し
# @app.route('/tweet_main', methods=["GET", "POST"])
# def main():
#     tweet_main()


if __name__ == '__main__':
    postgres_instance = Database.Database()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
