import os
from flask import Flask, request
from .information_gathering import tweet_main

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def login():
    if request.get_json()['API_KEY'] == os.environ.get('API_KEY'):
        # # 認証OKの場合
        return 200
    else:
        # 認証NGの場合
        return 401
    
    tweet_main()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
