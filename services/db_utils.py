import os
import sqlite3
from datetime import datetime, timedelta


def create_db():
    """Creates a new database, or connects to an existing one"""
    os.makedirs("./database", exist_ok=True)
    conn = sqlite3.connect("./database/files.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS Files")
    create_table_query = """CREATE TABLE Files (
                                filename VARCHAR(255) NOT NULL,
                                upload_time TEXT NOT NULL,
                                deletion_time TEXT
                            );
                        """
    cursor.execute(create_table_query)
    print("New table created")
    conn.close()


def init_fill_table(upload_folder):
    """Fills the table with filenames in the upload dir.
    This is meant to be run after freshly creating a database, in order to fil it with current data."""
    files = [
        f for f in os.listdir(upload_folder) if os.path.isfile(upload_folder + "/" + f)
    ]
    conn = sqlite3.connect("./database/files.db")
    cursor = conn.cursor()
    for file in files:
        cursor.execute(
            "INSERT INTO Files (filename, upload_time, deletion_time) VALUES(?, ?, ?)",
            (file, datetime.now(), datetime.now() + timedelta(hours=6)),
        )
    cursor.execute("SELECT * FROM Files")
    print(cursor.fetchall())
    conn.close()


def update_db(file):
    """This updates the table after every successful upload."""
    conn = sqlite3.connect("./database/files.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Files (filename, upload_time, deletion_time) VALUES(?, ?, ?)",
        (file, datetime.now(), datetime.now() + timedelta(hours=6)),
    )
    cursor.execute("SELECT * FROM Files WHERE filename=?", (file,))
    print(cursor.fetchall())
    conn.close()
