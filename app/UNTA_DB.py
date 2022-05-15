import sqlite3
import os
import datetime


def _connect_db(dbname="testi"):
    path = os.path.abspath(os.getcwd() + f"/data/{dbname}.db")
    if os.path.exists(path):
        return sqlite3.connect(path)
    return False


def _disconnect_db(connection):
    connection.close()


def _execute_db_query(query, dbname):
    connection = _connect_db(dbname)
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except sqlite3.Error as e:
        print("Database error: " + str(e))
    finally:
        _disconnect_db(connection)


def _execute_db_query_returnable(query, dbname):
    connection = _connect_db(dbname)
    rows = ""
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        print("Database error: " + str(e))

    _disconnect_db(connection)
    return rows


def create_db(dbname="testi"):
    path = os.path.abspath(os.getcwd() + f"/data/{dbname}.db")

    if not os.path.exists(path):
        _disconnect_db(sqlite3.connect(path))  # Connect and close connect to create db
        return "Database created with that name"

    return "Database exists with that name"


def create_table(table_name="testitaulu", dbname="testi"):
    connection = _connect_db(dbname)
    if not connection:
        return
    query = f"CREATE TABLE {table_name}(" \
            f"note_id INTEGER PRIMARY KEY , " \
            f"date_sub TEXT , " \
            f"title TEXT, " \
            f"content TEXT )"

    _execute_db_query(query, dbname)


def add_note(note_title, note_text, dbname="testi", table_name="testitaulu"):
    dt = datetime.datetime.now()
    dt = dt.strftime("%Y.%m.%d, %H.%M")

    query = f"INSERT INTO {table_name}(date_sub, title, content)" \
            f" VALUES (\'{dt}\', \'{note_title}\', \'{note_text}\');"

    _execute_db_query(query, dbname)


def delete_note(note_id, dbname="testi", table_name="testitaulu"):
    query = f"DELETE FROM {table_name} WHERE note_id={note_id};"
    _execute_db_query(query, dbname)


def list_all(dbname="testi", table_name="testitaulu"):
    query = f"SELECT note_id, date_sub, title FROM {table_name}"
    stuff = _execute_db_query_returnable(query, dbname)
    return stuff


def find_note(dbname="testi", table_name="testitaulu", noteid=None, note_title=None, note_time=None):
    query = None
    if noteid:
        query = f"SELECT note_id, date_sub, title FROM {table_name} WHERE note_id={noteid}"
        stuff = _execute_db_query_returnable(query, dbname)
        return stuff
    if note_title:
        query = f"SELECT note_id, date_sub, title FROM {table_name} WHERE title='{note_title}'"
        stuff = _execute_db_query_returnable(query, dbname)
        return stuff
    if noteid:
        query = f"SELECT note_id, date_sub, title FROM {table_name} WHERE date_sub='{note_time}'"
        stuff = _execute_db_query_returnable(query, dbname)
        return stuff


def read_note(note_id, dbname="testi", table_name="testitaulu"):
    stuff = None
    query = f"SELECT * FROM {table_name} WHERE note_id={note_id}"
    try:
        stuff = _execute_db_query_returnable(query, dbname)
    except:
        pass

    return stuff


def main():
    print(_connect_db())

    print(create_db())
    create_table()

    list = list_all()

    for row in list:
        print(row)


if __name__ == '__main__':
    main()
