# 导入mysql连接器/Python模块
import mysql.connector
import time
import xlsxwriter # type: ignore

# 定义连接参数
host = "localhost" # 你的mysql服务器地址
user = "root" # 你的mysql用户名
password = "" # 你的mysql密码

def init_db():
    # 建立连接，不指定数据库名
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    c = conn.cursor()

    # 列出所有的数据库名
    c.execute("SHOW DATABASES")
    databases = c.fetchall()

    # 判断目标数据库名是否存在
    database_exists = False
    for database in databases:
        if database[0] == "weibo_hot":
            database_exists = True
            break

    if database_exists:
        # 选择数据库
        c.execute("USE weibo_hot")
    else:
        # 创建数据库
        c.execute("CREATE DATABASE weibo_hot CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci")
        # 选择数据库
        c.execute("USE weibo_hot")

    # 检查表是否已经存在
    c.execute("SHOW TABLES")
    tables = c.fetchall()
    table_exists = False
    for table in tables:
        if table[0] == "weibo_hot":
            table_exists = True
            break

    if table_exists:
        # 检查表结构是否符合预期
        c.execute("DESCRIBE weibo_hot")
        table_info = c.fetchall()
        expected_table_info = [
            ("id", "int", "NO", "PRI", None, "auto_increment"),
            ("rank", "int", "YES", "", None, ""),
            ("url", "text", "YES", "", None, ""),
            ("keyword", "text", "YES", "", None, ""),
            ("num", "text", "YES", "", None, ""),
            ("timestamp", "int", "YES", "", None, ""),
        ]
        if table_info != expected_table_info:
            # 删除表并重新创建正确的结构
            c.execute("DROP TABLE IF EXISTS weibo_hot")
            c.execute(
                """CREATE TABLE weibo_hot (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    rank INT,
                    url TEXT,
                    keyword TEXT,
                    num TEXT,
                    timestamp INT
                )"""
            )
            conn.commit()
    else:
        # 创建表
        c.execute(
            """CREATE TABLE weibo_hot (
                id INT AUTO_INCREMENT PRIMARY KEY,
                rank INT,
                url TEXT,
                keyword TEXT,
                num TEXT,
                timestamp INT
            )"""
        )
        conn.commit()

    conn.close()


def export_to_xlsx():
    # 建立连接，指定数据库名
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database="weibo_hot"
    )
    c = conn.cursor()
    c.execute("SELECT * FROM weibo_hot")
    data = c.fetchall()
    conn.close()

    workbook = xlsxwriter.Workbook("weibo_hot.xlsx")
    worksheet = workbook.add_worksheet()

    # 写入表头
    headers = ["id", "rank", "url", "keyword", "num", "timestamp"]
    for i, header in enumerate(headers):
        worksheet.write(0, i, header)

    # 写入数据
    for row_num, row_data in enumerate(data):
        for col_num, col_data in enumerate(row_data):
            worksheet.write(row_num + 1, col_num, col_data)

    workbook.close()


def insert_data(data):
    # 建立连接，指定数据库名
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database="weibo_hot"
    )
    c = conn.cursor()
    for row in data:
        c.execute(
            """INSERT INTO weibo_hot (rank, url, keyword, num, timestamp)
               VALUES (%s, %s, %s, %s, %s)""",
            (*row, int(time.time())),
        )
    conn.commit()
    conn.close()


def get_data(timestamp):
    # 建立连接，指定数据库名
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database="weibo_hot"
    )
    c = conn.cursor()
    c.execute("SELECT * FROM weibo_hot WHERE timestamp=%s", (timestamp,))
    data = c.fetchall()
    conn.close()
    return data

def get_time():
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database="weibo_hot"
    )
    c = conn.cursor()
    c.execute("SELECT timestamp FROM weibo_hot")
    data = c.fetchall()
    conn.close()
    return data