import requests


def get_request(url):
    """
    getAPI用リクエスト

    Parameters
    ----------
    url : string
        リクエスト用url

    Returns
    -------
    request_data : dict
        jsonパースしたResponseデータ
    """
    return requests.get(url).json()


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


def post_request(url, payload):
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
    return requests.post(url, json=payload).json()


def put_request(url, payload):
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
    return requests.put(url, json=payload).json()


def delete_request(url):
    """
    getAPI用リクエスト

    Parameters
    ----------
    url : string
        リクエスト用url

    Returns
    -------
    request_data : dict
        jsonパースしたResponseデータ
    """
    return requests.delete(url).json()
