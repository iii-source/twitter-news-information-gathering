import json
import os
from functools import wraps
from jsonschema import validate, ValidationError
from flask import request

from common.response_message.error_response import error_response_400


# def validate_json(f):
#     @wraps(f)
#     def wrapper(*args, **kw):
#         if request.json is None:
#             return error_response_400()
#         else:
#             return f
#     return wrapper


def validate_schema(f):
    """
    jsonのbodyをjson schemaでkey,value,型チェックする

    Parameters
    ----------
    f : function
        呼び出し元の関数

    Returns
    -------
    error_response_400() or f(*args, **kw) : dict
        validateエラーかメイン処理の戻り値
    """
    @wraps(f)
    def wrapper(*args, **kw):
        # validateディレクトリへ移動
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # validateディレクトリの関数名と同名のjsonファイルを使用しjson schemaチェック
        # f.__name__ = 呼び出し元の関数名
        file_name = "{}/{}.json".format(os.getcwd(), f.__name__)
        with open(file_name) as file:
            schema = json.load(file)
        try:
            validate(request.json, schema)
        except ValidationError as e:
            return error_response_400()
        return f(*args, **kw)
    return wrapper
