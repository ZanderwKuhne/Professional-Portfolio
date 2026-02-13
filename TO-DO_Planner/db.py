import sqlite3
from pathlib import Path

# Setting up database directory path, if it already exists, continue
DB_DIR = Path("db_dir")
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "TD.db"


# Setup connection to the database using sqlite3, defining this as a function so this step is easy to repeat.
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Ensuring foreign keys are enabled and usable for this application
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


# Function for Initiating the database, called in main.py
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXIST users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            pass TEXT NOT NULL UNIQUE,
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXIST goals(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            goal TEXT NOT NULL,
            priority INTEGER NOT NULL,
            date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
            deadline DATETIME,
            min_time INTEGER,
            status TEXT NOT NULL

            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
