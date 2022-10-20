"""
Database connector/tools for MySQL/MariaDB server

Version: 0.1 (Major.Minor)
"""

from typing import Any
import pymysql
import pymysql.cursors
import os
import datetime
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()  # Load the dotenv file

# Global defines for MySQL database from dotenv
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')

"""
Main connector class for MySQL/MariaDB connections
"""


class DatabaseConnector:

    # Init the database connection
    def __init__(self) -> None:
        try:
            cnx = pymysql.connect(host=HOST, port=int(PORT), user=USERNAME,  # type: ignore
                                  password=PASSWORD, database=DATABASE, autocommit=True, cursorclass=pymysql.cursors.DictCursor) # type: ignore
            self.connection = cnx
            # cnx.close()
        except pymysql.Error as err:
            print(f"PyMySQL returned an error: {err}")

    def get_connection_object(self) -> pymysql.Connection:
        return self.connection


"""
Class containing main database query constructors
"""


class DatabaseQueries:

    def __init__(self, cnx: pymysql.Connection) -> None:
        self.cnx = cnx

    def insert_data(self, data: dict) -> bool:
        # timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        if data['operation'] != 'insert':
            raise TypeError(f"Incorrect query call for {data['operation']}")

        cursor = self.cnx.cursor()
        sql_string = self.__construct_query(data)

        try:
            cursor.execute(sql_string, data['data'])
            return True
        except Exception as ex:
            print(ex)
            return False

    def select_data(self, data: dict) -> Any:

        if data['operation'] != 'select' and data['operation'] != 'conditional_select':
            raise TypeError(f"Incorrect query call for {data['operation']}")

        cursor = self.cnx.cursor()
        sql_string = self.__construct_query(data)

        try:
            cursor.execute(sql_string, data['data'])
            return cursor.fetchall()
        except Exception as ex:
            print(ex)
            cursor.close()
            return False

    # INSERT Format: {'operation': 'insert', 'table': 'name', 'data': {'some': 'data', 'goes': 'here'}}
    # SELECT Format: {'operation': 'select', 'table': 'name', 'columns': ['col1', 'col2']}
    # CONDITIONAL SELECT Format: {'operation': 'conditional_select', 'table': 'name', 'condition': 'string', 'columns': ['col1', 'col2']}
    # TODO: Deletion and updating
    def __construct_query(self, data: dict) -> str:
        query_out = ""
        temp_keys = []
        table = data['table']

        if data['operation'] == 'insert':
            query_out += f"INSERT INTO {table} (" + ', '.join(
                list(data['data'].keys())) + ") VALUES ("

            for key in data['data']:
                temp_keys.append("%(" + key + ")s")

            query_out += ', '.join(temp_keys) + ")"

        elif data['operation'] == 'select':
            query_out += f"SELECT {', '.join(list(data['columns']))} "
            query_out += f"FROM {table}"

        elif data['operation'] == 'conditional_select':
            condition = data['condition']

            query_out += f"SELECT {', '.join(list(data['columns']))} "
            query_out += f"FROM {table} WHERE {condition}"

        else:
            raise NotImplementedError(
                "Unknown query method. Check that the correct query name is used.")

        return query_out
