import requests

URL_REF = 'https://iii-source.github.io/public/' \
          'swagger_ui/tweet_news/docs/dist/'


# 正常系 通常取得
def test_news_all01():
    # リクエストAPI用jsonデータ作成
    result = get_request(get_url())
    for i, record in enumerate(result['records']):
        if i == 0:
            assert record['newsid'] == 1
            assert record['news_date'] == '2020-08-07'
            assert record['url'] == 'https://hogehoge1'
            assert record['description'] == '説明を日本語で記す'
        elif i == 1:
                assert record['newsid'] == 2
                assert record['news_date'] == '2020-08-09'
                assert record['url'] == 'https://hogehoge2'
                assert record['description'] == 'english discription1'
        else:
            break


def get_url():
    # テスト対象のURLを定義
    return 'http://localhost:5000/news/'


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
