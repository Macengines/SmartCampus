import os
from flask import Flask, jsonify, request, g
import json
import pymysql

app = Flask(__name__)

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'strong_password05.',
    'database': 'poly_eng_app',
    'port': 3306,
    'cursorclass': pymysql.cursors.DictCursor  # return results as dicts
}

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Folder to store uploaded files
UPLOAD_FOLDER = 'Server'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database connection setup
@app.before_request
def connect_db():
    """Establish a database connection before handling the request."""
    if 'db' not in g:
        g.db = pymysql.connect(**MYSQL_CONFIG)
        g.cursor = g.db.cursor()

@app.teardown_request
def close_db(exception=None):
    """Close the database connection after handling the request."""
    db = g.pop('db', None)
    if db:
        db.close()

# Route to notes table
@app.route('/api/news', methods=['GET'])
def fetch_news():
    g.cursor.execute("SELECT * FROM notes")
    news_list = g.cursor.fetchall()
    return jsonify(news_list)

if __name__ == '__main__':
    app.run(debug=True)