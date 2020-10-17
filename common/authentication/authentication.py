import json
import datetime
from common.db import Database as Database
from functools import wraps
from flask import request
from app import sql_id_yaml
from common.response_message import error_response


EXPIRATION_TIME = datetime.timedelta(hours=3)


def check_headers_uuid(postgres_instance):
    """
    認証後、発行されたuuidがheaderに付与されているか、一致しているかチェックする

    Parameters
    ----------

    Returns
    -------
    error_response_403() or f(*args, **kw) : dict
        validateエラーかメイン処理の戻り値
    """
    try:
        x_request_id = request.headers['X-Request-ID']
    except KeyError:
        # ヘッダーにX-Request-IDが付与されていなかった場合
        return error_response.error_response_403_no_uuid()
    # X-Request-IDをkeyにしてDB検索

    users_login_data = postgres_instance.select(
        sql_id_yaml['get_users_login'],
        x_request_id
    )
    # X-Request-ID(uuid)が存在しなかった場合
    if users_login_data.get('code') == 404:
        # return wrapper
        return error_response.error_response_403_expired_or_incorrect_uuid()

    login_time = users_login_data['records'][0]['login_time']
    # 現在時刻取得
    now_time = datetime.datetime.now()
    if EXPIRATION_TIME > (now_time - login_time):
        # X-Request-IDが一致している + 有効期限内だった場合 次の処理へ進む
        print("有効期限内")
        return 'OK'
    elif EXPIRATION_TIME <= (now_time - login_time):
        # X-Request-IDが一致していない or 有効期限外だった場合
        print("有効期限切れ")
        return error_response.error_response_403_expired_or_incorrect_uuid()
