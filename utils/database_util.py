

import pyodbc
import pandas as pd
from contextlib import contextmanager
from configs.user_constants import default_db_vars


class DBUtils:
    """ """
    def __init__(self, env=None, host=None, db_user=None, db_pass=None, db_instance=None, port=None):
        """ """
        if env == 'UAT':
            self.host = host
            self.db_user = db_user
            self.db_pass = db_pass
            self.db_instance = db_instance
            self.port = port
        else:
            self.host = host
            self.db_user = db_user
            self.db_pass = db_pass
            self.db_instance = db_instance
            self.port = port

    @contextmanager
    def connection(self):
        """ """
        connection = pyodbc.connect(self.conn_str)
        try:
            yield connection
        except pyodbc.DatabaseError as exp:
            connection.close()
            raise exp
        finally:
            connection.close()

    @contextmanager
    def cursor(self, commit=False):
        """ """
        connection = pyodbc.connect(self.conn_str)
        cursor = connection.cursor()
        try:
            yield cursor
        except pyodbc.DatabaseError as exp:
            cursor.rollback()
            raise exp
        else:
            if commit:
                cursor.commit()
        finally:
            cursor.close()
            connection.close()

    def execute_and_fetch_one(self, query):
        """ """
        if not isinstance(query, str):
            raise Exception(f"Query should be a string value, instead we got {type(query)}")

        try:
            with self.cursor() as cur:
                cur.execute(query)
                records = self.cursor.fetchone()
            return records
        except pyodbc.DatabaseError as exp:
            raise exp

    def execute_and_fetch_all(self, query):
        """ """
        if not isinstance(query, str):
            raise Exception(f"Query should be a string value, instead we got {type(query)}")

        try:
            with self.cursor() as cur:
                cur.execute(query)
                records = self.cursor.fetchall()
            return records
        except pyodbc.DatabaseError as exp:
            raise exp

    def execute_and_fetch_many(self, query, no_of_rows):
        """ """
        if not isinstance(query, str):
            raise Exception(f"Query should be a string value, instead we got {type(query)}")
        if not isinstance(no_of_rows, int):
            raise Exception(f"Query should be a string value, instead we got {type(no_of_rows)}")

        try:
            with self.cursor() as cur:
                cur.execute(query)
                records = self.cursor.fetchmany(no_of_rows)
            return records
        except pyodbc.DatabaseError as exp:
            raise exp

    def execute_and_fetch_dataframe(self, query, no_of_rows):
        """ """
        if not isinstance(query, str):
            raise Exception(f"Query should be a string value, instead we got {type(query)}")
        if not isinstance(no_of_rows, int):
            raise Exception(f"Query should be a string value, instead we got {type(no_of_rows)}")

        try:
            with self.connection() as conn:
                df = pd.read_sql_query(query, con=conn)
            return df
        except pyodbc.DatabaseError as exp:
            raise exp
