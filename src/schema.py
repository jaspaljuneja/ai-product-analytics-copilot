import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "src", "data", "analytics.db")

def get_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)

    tables = cursor.fetchall()

    schema_text = ""

    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        schema_text += f"\nTable: {table_name}\n"

        for column in columns:
            column_name = column[1]
            column_type = column[2]

            schema_text += f"- {column_name} ({column_type})\n"

    conn.close()

    return schema_text


if __name__ == "__main__":
    print(get_schema())
