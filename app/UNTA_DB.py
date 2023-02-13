import sqlite3
import os
import datetime


_DB_HANDLER = None

def _connect_db(dbname):
    global _DB_HANDLER
    
    path = os.path.abspath(os.getcwd() + f"/data/{dbname}.db")
    
    if _DB_HANDLER == sqlite3.connect(path):
        return True
    
    if os.path.exists(path):
        _DB_HANDLER = sqlite3.connect(path)
        return True
    
    return False


if not _connect_db("default"):
    raise RuntimeError("Database init error")


def disconnect_db():
    global _DB_HANDLER
    _DB_HANDLER.close()


def _execute_db_query(query):
    if not _DB_HANDLER:
        raise RuntimeError("Database connection lost")
    try:
        cursor = _DB_HANDLER.cursor()
        cursor.execute(query)
        _DB_HANDLER.commit()
    except sqlite3.Error as e:
        print("Database error: " + str(e))


def _execute_db_query_returnable(query):
    rows = ""

    try:
        cursor = _DB_HANDLER.cursor()
        cursor.execute(query)
        _DB_HANDLER.commit()
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        print("Database error: " + str(e))

    return rows


def create_db(dbname=None):
    global _DB_HANDLER
    
    if not dbname:
        _DB_HANDLER = sqlite3.connect(":memory:")
        return "In memory database created. FOR TESTING PURPOSES ONLY!"

    path = os.path.abspath(os.getcwd() + f"/data/{dbname}.db")

    if not os.path.exists(path):
        sqlite3.connect(path).close  # Connect and close connect to create db
        _connect_db(dbname)
        return "Database created with that name and connection estabished for that database"

    return "Database exists with that name"


def create_table(table_name):
    
    if not _DB_HANDLER:
        raise RuntimeError("Database connection lost")
    
    query = f"CREATE TABLE {table_name}(" \
            f"note_id INTEGER PRIMARY KEY , " \
            f"date_sub TEXT , " \
            f"date_edited TEXT , " \
            f"title TEXT, " \
            f"content TEXT )"

    _execute_db_query(query)


def add_note(note_title, note_text, table_name):
    dt = datetime.datetime.now()
    dt = dt.strftime("%Y.%m.%d, %H.%M")

    query = f"INSERT INTO {table_name}(date_sub, title, content)" \
            f" VALUES (\'{dt}\', \'{note_title}\', \'{note_text}\');"

    _execute_db_query(query)


def delete_note(note_id, table_name):
    query = f"DELETE FROM {table_name} WHERE note_id={note_id};"
    _execute_db_query(query)


def find_note(table_name, condition=None):
    """
    Creates a sql search query. If no condition is given, returns everything from a table.
    """
    query = None

    if not condition:
        query = f"SELECT note_id, date_sub, title FROM {table_name}"
    else:
        query = f"SELECT note_id, date_sub, title FROM {table_name} WHERE {condition}"
    
    stuff = _execute_db_query_returnable(query)
    return stuff


def read_note(note_id, table_name):
    stuff = None
    query = f"SELECT * FROM {table_name} WHERE note_id={note_id}"
    try:
        stuff = _execute_db_query_returnable(query)
    except:
        pass

    return stuff


def main():
    pass


if __name__ == '__main__':
    main()
