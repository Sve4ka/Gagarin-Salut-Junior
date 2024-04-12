import os
import psycopg2 as psql
from config import NAME_DB, NAME_U, PASS, HOST

conn = psql.connect(dbname=NAME_DB, user=NAME_U,
                    password=PASS, host=HOST)
cur = conn.cursor()


def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS "
                "user_table("
                "id SERIAL PRIMARY KEY, "
                "tg_id INTEGER,"
                "telephone VARCHAR(15), "
                "email VARCHAR(25))")
    conn.commit()

def add_deader(*args):
    pass

def add_db(text: str, *args) -> None:
    connect = psql.connect(dbname=NAME_DB, user=NAME_U, password=PASS, host=HOST)
    cursor = connect.cursor()
    cursor.execute(text, args)
    cursor.close()
    connect.commit()
    connect.close()


def answer_bd(text: str, *args) -> list:
    connect = psql.connect(dbname=NAME_DB, user=NAME_U, password=PASS, host=HOST)
    cursor = connect.cursor()
    cursor.execute(text, args)
    answer = cursor.fetchall()
    cursor.close()  # закрываем курсор
    connect.close()
    return answer



def add_user(id_user: int, phone: str, email: str) -> None:
    sql_query = "insert into user_table values (%s, %s, %s, %s)"
    add_db(sql_query, free_user_id(), id_user, phone, email)


def free_user_id() -> int:
    all_users = answer_bd("SELECT * FROM user_table")
    if all_users:
        return max([i[0] for i in all_users]) + 1
    return 1

def search_id_user(id_user: int) -> int:
    users = answer_bd("SELECT * FROM user_table WHERE tg_id=%s", id_user)
    if len(users) == 0:
        return 0
    return users[0][0]