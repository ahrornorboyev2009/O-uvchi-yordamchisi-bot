import sqlite3

DB_NAME = "students.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            score INTEGER,
            total INTEGER
        )
    """)

    conn.commit()
    conn.close()


def add_user(user_id, username, first_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO users (id, username, first_name)
        VALUES (?, ?, ?)
    """, (user_id, username, first_name))

    conn.commit()
    conn.close()


def save_result(user_id, subject, score, total):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO test_results (user_id, subject, score, total)
        VALUES (?, ?, ?, ?)
    """, (user_id, subject, score, total))

    conn.commit()
    conn.close()


def get_results(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subject, score, total
        FROM test_results
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    results = cursor.fetchall()

    conn.close()

    return results