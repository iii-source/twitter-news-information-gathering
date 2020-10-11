import time
import json
import os
import pprint
from dateutil.parser import parse
from datetime import datetime
from requests_oauthlib import OAuth1Session


CONSUMER_KEY_TWEET_NEWS = os.environ['CONSUMER_KEY_TWEET_NEWS']
CONSUMER_SECRET_TWEET_NEWS = os.environ['CONSUMER_SECRET_TWEET_NEWS']
ACCESS_TOKEN_TWEET_NEWS = os.environ['ACCESS_TOKEN_TWEET_NEWS']
ACCESS_TOKEN_SECRET_TWEET_NEWS = os.environ['ACCESS_TOKEN_SECRET_TWEET_NEWS']

twitter = OAuth1Session(CONSUMER_KEY_TWEET_NEWS, CONSUMER_SECRET_TWEET_NEWS,
                        ACCESS_TOKEN_TWEET_NEWS, ACCESS_TOKEN_SECRET_TWEET_NEWS)


# メイン処理
def tweet_main():
    # 1 タイムライン取得
    req, timeline_list = get_timeline()

    result_list = []
    # news_data, url, title, description を返却用に加工し格納
    for timeline in timeline_list['statuses']:
        news_dict = {}
        # ツイート生成時刻の取得 + フォーマット成型
        news_dict['news_date'] = parse(timeline['created_at']).strftime('%Y-%m-%d %H:%M:%S')
        # #nhk_newsでtitle + url を分割
        title_url = timeline['text'].split('#nhk_news')
        news_dict['url'] = title_url[1].strip()
        news_dict['title'] = title_url[0]
        news_dict['description'] = ""

        result_list.append(news_dict)

    # API使用回数取得
    # リクエスト可能残数の取得
    limit = req.headers['x-rate-limit-remaining']
    # リクエスト叶残数リセットまでの時間(UTC)
    reset = req.headers['x-rate-limit-reset']
    # UTCを秒数に変換
    sec = int(req.headers['X-Rate-Limit-Reset']) - time.mktime(datetime.now().timetuple())
    # API使用回数表示 デバッグ用
    print("limit: " + limit)
    print("reset: " + reset)
    print('reset sec:  %s' % sec)
    pprint.pprint(result_list)

    return result_list


# 1 検索結果取得
def get_timeline():
    # TODO 検索条件を外部定義し動的に変更可能にする
    params = {'q': 'from:nhk_news 埼玉 新型コロナ'}
    search_tweets_url = 'https://api.twitter.com/1.1/search/tweets.json'
    req = twitter.get(search_tweets_url, params=params)
    timeline = json.loads(req.text)
    return req, timeline


if __name__ == '__main__':
    tweet_main()
