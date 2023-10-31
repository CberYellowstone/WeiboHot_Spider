import time
from flask import Flask, request
import sqlite3

app = Flask(__name__)


@app.route("/table")
def display_table():
    timestamp = request.args.get("timestamp")

    conn = sqlite3.connect("database.sqlite3")
    c = conn.cursor()

    c.execute("SELECT * FROM weibo_hot WHERE timestamp=?", (timestamp,))
    data = c.fetchall()

    table_html = "<table>"
    table_html += "<tr><th>ID</th><th>Rank</th><th>Keyword</th><th>Num</th><th>Timestamp</th></tr>"
    for row in data:
        table_html += "<tr>"
        table_html += "<td>{}</td><td>{}</td><td onclick=\"window.open('{}');\">{}</td><td>{}</td><td>{}</td>".format(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(row[5])),
        )
        table_html += "</tr>"
    table_html += "</table>"

    conn.close()

    return table_html


@app.route("/")
def display_optional_time():
    conn = sqlite3.connect("database.sqlite3")
    c = conn.cursor()

    c.execute("SELECT timestamp FROM weibo_hot")
    data = c.fetchall()

    conn.close()

    time_list = []
    for row in data:
        time_list.append(row[0])

    time_list = list(set(time_list))
    time_list.sort(reverse=True)

    time_html = "<h2>请选择一个时间</h2>"
    for timestamp in time_list:
        time_html += '<a href="/table?timestamp={}">{}</a><br>'.format(
            timestamp, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        )

    return time_html


if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://localhost:5000/")
    app.run(debug=True, port=5000)
