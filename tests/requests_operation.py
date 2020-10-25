import requests

auth_url = 'http://localhost:5000/user/login'


def get_request(url, headers):
    """
    getAPI用リクエスト

    Parameters
    ----------
    url : string
        リクエスト用url
    headers : dict
        認可用uuid

    Returns
    -------
    request_data : dict
        jsonパースしたResponseデータ
    """
    return requests.get(url, headers=headers).json()


def get_request_with_auth(user, password):
    """
    getAPI用リクエスト(Basic認証用)

    Parameters
    ----------
    user : string
        basic認証用user
    password : string
        basic認証用password

    Returns
    -------
    result : dict
        jsonパースした(or そのままの)Responseデータ
    """
    result = requests.get(auth_url, auth=(user, password), verify=False)
    if 'json' in result.headers.get('content-type'):
        # application/jsonの場合jsonDecodeで返す
        return result.json()
    else:
        # text/htmlの場合そのまま返す
        return result


def get_request_with_body(url, payload):
    """
    getAPI用リクエスト

    Parameters
    ----------
    url : string
        リクエスト用url
    payload : dict
        リクエスト用データ

    Returns
    -------
    request_data : dict
        jsonパースしたResponseデータ
    """
    return requests.get(url, json=payload).json()


def post_request(url, payload, headers):
    """
    getAPI用リクエスト

    Parameters
    ----------
    url : string
        リクエスト用url
    payload : dict
        リクエスト用データ
    headers : dict
        認可用uuid

    Returns
    -------
    request_data : dict
        jsonパースしたResponseデータ
    """
    return requests.post(url, json=payload, headers=headers).json()


def put_request(url, payload, headers):
    """
    getAPI用リクエスト

    Parameters
    ----------
    url : string
        リクエスト用url
    payload : dict
        リクエスト用データ
    headers : dict
        認可用uuid

    Returns
    -------
    request_data : dict
        jsonパースしたResponseデータ
    """
    return requests.put(url, json=payload, headers=headers).json()


def delete_request(url, headers):
    """
    getAPI用リクエスト

    Parameters
    ----------
    url : string
        リクエスト用url
    headers : dict
        認可用uuid

    Returns
    -------
    request_data : dict
        jsonパースしたResponseデータ
    """
    return requests.delete(url, headers=headers).json()
