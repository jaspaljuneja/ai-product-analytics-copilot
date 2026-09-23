import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "src", "data", "analytics.db")


def run_sql(query, conn=None):

    if conn is None:
        conn = sqlite3.connect(DB_PATH)
        close_connection = True
    else:
        close_connection = False

    cursor = conn.cursor()

    cursor.execute(query)

    results = cursor.fetchall()

    column_names = [
        description[0]
        for description in cursor.description
    ]

    if close_connection:
        conn.close()

    return column_names, results
