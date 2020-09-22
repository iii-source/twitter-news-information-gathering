import uuid
import datetime
from app import sql_id_yaml

# 有効期限 3時間
EXPIRATION_TIME = datetime.timedelta(hours=3)


class AuthorizationUuid:
    def __init__(self, postgres_instance, auth):
        self.postgres_instance = postgres_instance
        self.auth = auth
        # 現在時刻を取得
        self.now_time = datetime.datetime.now()
        # users_loginのデータ取得
        self.__get_users_login()

    # users_login情報取得
    def __get_users_login(self):
        self.get_results = self.postgres_instance.select(
            sql_id_yaml['get_users_login'],
            self.auth.username()
        )

    # users_loginのtokenとlogin_timeを更新する
    def __put_token_login_time(self):
        self.postgres_instance.update(
            sql_id_yaml['put_users_login_token_login_time'],
            *(self.token, self.now_time),
            where_id=self.auth.username()
        )

    # users_loginのlogin_timeを更新する
    def __put_login_time(self):
        self.postgres_instance.update(
            sql_id_yaml['put_users_login_login_time'],
            self.now_time,
            where_id=self.auth.username()
        )

    # uuidのチェック
    def __create_check_token(self):
        # 既存のtokenとは別のtokenを生成する(入れ替え用)
        __token = str(uuid.uuid4())
        while True:
            # 生成したtokenと既存のtokenが不一致であれば新しいtokenを返却
            if not(__token == self.get_results['records'][0]['token']):
                self.token = __token
                break
        # 存在していた場合は再度uuidを作成、検索
            __token = str(uuid.uuid4())

    # uuidを生成して返却
    def users_login(self):
        # ログインユーザーの最終ログイン時刻を取得
        login_time = self.get_results['records'][0]['login_time']

        if EXPIRATION_TIME > (self.now_time - login_time):
            print("有効期限内")
            # nowの方が小さい場合有効期限内 その時は既存のlogin_timeを更新(uuidはそのまま)
            self.__put_login_time()
        elif EXPIRATION_TIME <= (self.now_time - login_time):
            print("有効期限切れ")
            # 更新用のtokenを生成する。
            self.__create_check_token()
            # nowの方が大きいので有効期限切れ tokenとlogin_timeを更新
            self.__put_token_login_time()

        # 更新後のデータを返却用に取得
        self.__get_users_login()

        return self.get_results
