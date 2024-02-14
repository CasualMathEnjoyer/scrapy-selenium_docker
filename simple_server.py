import http.server
import socketserver
import os
import psycopg2
from html import escape

import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("Server starting")

db_params = {
        'user': 'docker',
        'password': 'docker',
        'host': 'database',
        'port': '5432',
        'database': 'exampledb',
    }

SQL_QUERY = "SELECT * FROM sreality"

def fetch_data():
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        cursor.execute(SQL_QUERY)
        data = cursor.fetchall()
        print("Connected to the database!")
        logging.debug("Connected to the database!")
        return data
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        logging.debug(f"Error connecting to the database: {e}")
        return []

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            print("fetching data")
            logging.debug("fetching data")
            data = fetch_data()

            html_content = "<html><head><title>Database Elements</title></head><body>"
            html_content += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />"
            html_content += "<ul>"
            if data == []:
                html_content += "Data not scraped yet, please refresh"
            for row in data:
                html_content += f"<p> {row[0]}. {escape(row[1])}</p>"
                html_content += f"<img src='{escape(row[2])}' alt='Image' width='200'>"
            html_content += "</ul>"
            html_content += "</body></html>"

            self.wfile.write(html_content.encode())
        else:
            super().do_GET()

def run_server(host, port):
    try:
        with socketserver.TCPServer((host, port), MyHandler) as server:
            print(f"Serving on http://{host}:{port}")
            logging.debug(f"Serving on http://{host}:{port}")
            server.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down...")
        logging.debug("Server shutting down...")

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8080
    run_server(HOST, PORT)
