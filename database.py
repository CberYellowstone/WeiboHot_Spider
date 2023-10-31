import sqlite3
import time
import xlsxwriter


def init_db():
    conn = sqlite3.connect("database.sqlite3")
    c = conn.cursor()

    # Check if table already exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weibo_hot'")
    table_exists = c.fetchone()

    if table_exists:
        # Check if table schema is as expected
        c.execute("PRAGMA table_info('weibo_hot')")
        table_info = c.fetchall()
        expected_table_info = [
            (0, "id", "INTEGER", 0, None, 1),
            (1, "rank", "INTEGER", 0, None, 0),
            (2, "url", "TEXT", 0, None, 0),
            (3, "keyword", "TEXT", 0, None, 0),
            (4, "num", "INTEGER", 0, None, 0),
            (5, "timestamp", "INTEGER", 0, None, 0),
        ]
        if table_info != expected_table_info:
            # Drop table and recreate with correct schema
            c.execute("DROP TABLE IF EXISTS weibo_hot")
            c.execute(
                """CREATE TABLE weibo_hot
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          rank INTEGER,
                          url TEXT,
                          keyword TEXT,
                          num INTEGER,
                          timestamp INTEGER)"""
            )
            conn.commit()
    else:
        # Create table
        c.execute(
            """CREATE TABLE weibo_hot
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      rank INTEGER,
                      url TEXT,
                      keyword TEXT,
                      num INTEGER,
                      timestamp INTEGER)"""
        )
        conn.commit()

    conn.close()


def export_to_xlsx():
    conn = sqlite3.connect("database.sqlite3")
    c = conn.cursor()
    c.execute("SELECT * FROM weibo_hot")
    data = c.fetchall()
    conn.close()

    workbook = xlsxwriter.Workbook("weibo_hot.xlsx")
    worksheet = workbook.add_worksheet()

    # Write headers
    headers = ["id", "rank", "url", "keyword", "num", "timestamp"]
    for i, header in enumerate(headers):
        worksheet.write(0, i, header)

    # Write data
    for row_num, row_data in enumerate(data):
        for col_num, col_data in enumerate(row_data):
            worksheet.write(row_num + 1, col_num, col_data)

    workbook.close()


def insert_data(data):
    conn = sqlite3.connect("database.sqlite3")
    c = conn.cursor()
    for row in data:
        c.execute(
            "INSERT INTO weibo_hot (rank, url, keyword, num, timestamp) VALUES (?, ?, ?, ?, ?)",
            (*row, int(time.time())),
        )
    conn.commit()
    conn.close()
