from typing import Dict
import psycopg2
import json
from dotenv import load_dotenv
import os
load_dotenv()

CREATE_DATABASE = """CREATE DATABASE ResumeBuilderDB; """

CREATE_USERALL_TABLE = """CREATE TABLE IF NOT EXISTS UsersAll (

    user_id VARCHAR(50),
    data JSONB

); """

INSER_USER_DATA = """INSERT INTO UsersAll (user_id, data) VALUES (%s, %s)"""

GET_USER_DATA = """
    SELECT * FROM UsersAll WHERE user_id = %s;
"""

GET_TABLE_NAMES = """
    SELECT tablename FROM pg_catalog.pg_tables 
    WHERE schemaname NOT IN ('pg_catalog', 'information_schema');
    """

UPDATE_DATA = """ UPDATE UsersAll
SET data = %s WHERE user_id = %s ;
 """
# conn_url = os.environ["DATABASE_URI"]
# connection = psycopg2.connect(conn_url)


def create_table(connection) -> None:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_USERALL_TABLE)


def inser_user_data(connection, user_id:str, data:dict) -> None:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSER_USER_DATA, (user_id, json.dumps(data)))


def get_user_data(connection, user_id:str) -> Dict :  ##
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(GET_USER_DATA, (str(user_id),))
            return cursor.fetchall()


def list_tables(connection) -> None:
    with connection:
        with connection.cursor() as cursor:
            list_of_tables = cursor.execute(GET_TABLE_NAMES)
            print([table[0] for table in cursor.fetchall()])


def edit_data(connection,user_id: str, data: dict) -> None:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_DATA, (json.dumps(data), user_id))
