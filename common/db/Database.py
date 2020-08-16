from psycopg2.extras import DictCursor, psycopg2
from common.db import LOGGING_PATH, LOGGING_PATH_CURRENT, sql_yaml
from common.response_message import response, error_response
import logging
import os


class Database:
    def __init__(self):
        try:
            self.connector = psycopg2.connect(os.environ.get("DATABASE_URL"))
        except psycopg2.OperationalError as e:
            logging.error('40', exc_info=True)
            raise e
        self.cursor = self.connector.cursor(cursor_factory=DictCursor)

    def get_cursor(self):
        self.cursor = self.connector.cursor(cursor_factory=DictCursor)

    def release_cursor(self):
        self.cursor.close()

    def select(self, sql_id_yaml, *where_id):
        # カーソル取得
        self.get_cursor()
        stmt = sql_yaml[sql_id_yaml]
        try:
            self.cursor.execute(stmt, (where_id,))
        except (psycopg2.errors.UndefinedColumn,
                psycopg2.errors.InvalidTextRepresentation):
            logging.error('30', exc_info=True)
            self.connector.rollback()
            return error_response.error_response_400()
        except psycopg2.errors.InFailedSqlTransaction:
            # カーソル解放失敗した場合など
            logging.error('40', exc_info=True)
            self.connector.rollback()
            return error_response.error_response_500()

        try:
            if sql_id_yaml.rfind('ALL'):
                # 複数レコードの場合
                result = self.cursor.fetchall()
            else:
                # 単数レコードの場合
                result = self.cursor.fetchone()
        except psycopg2.ProgrammingError:
            logging.error('30', exc_info=True)
            return error_response.error_response_400()

        # レコードが0件の場合
        if len(result) == 0:
            return response.response_404()

        result_list = []
        result_dict = {}
        # TODO jsonで返す時、順番が反転してしまう問題
        for row in result:
            # DictRowをdict変換
            result_list.append(dict(row))
        result_dict['records'] = result_list

        # カーソル解放
        self.release_cursor()
        return result_dict

    def insert(self, sql_id_yaml, set_value):
        self.get_cursor()
        stmt = sql_yaml[sql_id_yaml]
        try:
            self.cursor.execute(stmt, set_value)
        except (psycopg2.errors.UndefinedColumn,
                psycopg2.errors.InvalidTextRepresentation):
            logging.error('30', exc_info=True)
            self.connector.rollback()
            return error_response.error_response_400()
        except psycopg2.errors.InFailedSqlTransaction:
            # カーソル解放失敗した場合など
            logging.error('40', exc_info=True)
            self.connector.rollback()
            return error_response.error_response_500()

        # レコードが0件の場合
        if self.cursor.fetchone() is None:
            return response.response_404()

        # updateが正常終了した場合
        # カーソル解放
        self.release_cursor()
        self.connector.commit()
        return response.response_200_post()

    def update(self, sql_id_yaml, set_value, where_id):
        self.get_cursor()
        stmt = sql_yaml[sql_id_yaml]
        try:
            self.cursor.execute(stmt, (set_value, where_id))
        except (psycopg2.errors.UndefinedColumn,
                psycopg2.errors.InvalidTextRepresentation):
            logging.error('30', exc_info=True)
            self.connector.rollback()
            return error_response.error_response_400()
        except psycopg2.errors.InFailedSqlTransaction:
            # カーソル解放失敗した場合など
            logging.error('40', exc_info=True)
            self.connector.rollback()
            return error_response.error_response_500()

        # レコードが0件の場合
        if self.cursor.fetchone() is None:
            return response.response_404()

        # updateが正常終了した場合
        # カーソル解放
        self.release_cursor()
        self.connector.commit()
        return response.response_200_put()

    # TODO メンテナンス用
    def close(self):
        self.cursor.close()
        self.connector.close()


if __name__ == '__main__':
    postgres_instance = Database()
    logging.basicConfig(filename=LOGGING_PATH_CURRENT)
else:
    # server.pyからの相対パス
    logging.basicConfig(filename=LOGGING_PATH)

