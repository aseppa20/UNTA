import pytest
import os
import app.UNTA_DB as UDB
import time


tbl = "testtable"

@pytest.fixture(autouse=True)
def init():
    UDB.create_db()
    UDB.create_table(tbl)
    
    yield

    UDB.disconnect_db()


def test_database_add_and_read_note():
    UDB.add_note("Test", "This is a test note", tbl)
    assert str(UDB.find_note(tbl)).find("Test") + 1  


def test_database_add_and_remove_note():
    UDB.add_note("Test", "This is a test note", tbl)
    assert str(UDB.find_note(tbl)).find("Test") + 1  
    UDB.delete_note(1, tbl)
    assert not str(UDB.find_note(tbl)).find("Test") + 1
    