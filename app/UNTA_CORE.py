import UNTA_DB

# Global variables for DB testing, to be replaced with something better
_DBNAME = "testi"
_DB_TABLE = "testitaulu"


def add_note(note_title, note):
    if len(note_title) > 255:
        raise Exception("Title too long (over 255 characters)")

    UNTA_DB.add_note(note_title, note, _DBNAME, _DB_TABLE)


def list_all_notes():
    rows = UNTA_DB.list_all(_DBNAME, _DB_TABLE)
    data = ""
    for row in rows:
        data = data + f"id: {row[0]}, date: {row[1]}, title: {row[2]} \n"

    return data


def read_note(note_id):
    try:
        row = UNTA_DB.read_note(note_id, _DBNAME, _DB_TABLE).pop()
        note = f"id: {row[0]}, date: {row[1]} \n" \
               f"title: {row[2]} \n" \
               f"{row[3]}"

        return note
    except:
        pass


def remove_note():
    pass


def main():
    print(list_all_notes())
    print(read_note(2))


if __name__ == '__main__':
    main()
