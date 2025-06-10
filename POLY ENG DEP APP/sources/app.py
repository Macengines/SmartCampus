import os
import json
from flask import Flask, jsonify, request, g
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mactech',
    'database': 'poly_eng_app',
    'port': 3305
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
        g.db = mysql.connector.connect(**MYSQL_CONFIG)
        g.cursor = g.db.cursor(dictionary=True)

@app.teardown_request
def close_db(exception=None):
    """Close the database connection after handling the request."""
    db = g.pop('db', None)
    if db:
        db.close()

@app.route('/upload_vid', methods=['POST'])
def upload_vid():
    file = request.files.get('file')
    if file:
        try:
            department = "civil engineering"
            course_name = "civil proper"
            level = "nd2"
            category = "notes"
            # Save the file
            notes_folder = os.path.join(app.config['UPLOAD_FOLDER'],department, course_name, level, category)
            file_path = os.path.join(notes_folder, file.filename)
            file.save(file_path)

            # Insert metadata into the database
            file_name = file.filename
            file_size = os.path.getsize(file_path)
            file_type = os.path.splitext(file_name)[1]  # Extract the file extension
            file_name_without_extension = os.path.splitext(file_name)[0]

            # Use the shared database connection
            g.cursor.execute(
                "INSERT INTO notes (name, size, path, type) VALUES (%s, %s, %s, %s)",  # Include `type`
                (file_name_without_extension, file_size, file_path, file_type)  # Add `file_type` as a value
            )

            g.db.commit()

            return jsonify({'message': 'File uploaded and metadata saved successfully!', 'file': file_name}), 200
        except Exception as file_error:
            return jsonify({'message': f'Error saving file: {str(file_error)}'}), 500
    return jsonify({'message': 'No file uploaded!'}), 400

@app.route('/api/notes', methods=['GET'])
def get_notes():

    
    with open("students.json", "r") as f:
        details = json.load(f)
        dept = details.get("DEPARTMENT", "")
        course = details.get("COURSE", "")
        level = details.get("LEVEL", "")
    
    sql = """
        SELECT * FROM Content
        WHERE department = %s AND course = %s AND level = %s AND content_type = "note"
    """
    g.cursor.execute(sql,(dept,course,level))
    results = g.cursor.fetchall()
    g.cursor.close()

    return jsonify(results)

@app.route('/api/images', methods=['GET'])
def get_images():
    with open("students.json", "r") as f:
        details = json.load(f)
        dept = details.get("DEPARTMENT", "")
        course = details.get("COURSE", "")
        level = details.get("LEVEL", "")

    sql = """
        SELECT * FROM Content
        WHERE department =%s AND course = %s AND level = %s AND content_type = "image"
    """
    g.cursor.execute(sql,(dept,course,level))
    files_list = g.cursor.fetchall()
    return jsonify(files_list)

@app.route('/api/videos', methods=['GET'])
def get_videos():
    with open("students.json", "r") as f:
        details = json.load(f)
        dept = details.get("DEPARTMENT", "")
        course = details.get("COURSE", "")
        level = details.get("LEVEL", "")

    sql = """
        SELECT * FROM Content
        WHERE department =%s AND course = %s AND level = %s AND content_type = "video"
    """
    g.cursor.execute(sql,(dept,course,level))
    files_list = g.cursor.fetchall()
    return jsonify(files_list)

@app.route('/api/news', methods=['GET'])
def fetch_news():
    g.cursor.execute("SELECT * FROM news")
    news_list = g.cursor.fetchall()
    return jsonify(news_list)

@app.route('/api/news2', methods=['GET'])
def fetch_news2():
    g.cursor.execute("SELECT * FROM news2")
    news_list = g.cursor.fetchall()
    return jsonify(news_list)

@app.route('/api/zuva', methods=['GET'])
def fetch_zuva():
    g.cursor.execute("SELECT * FROM zuva")
    zuva_list = g.cursor.fetchall()
    return jsonify(zuva_list)



if __name__ == '__main__':
    app.run(debug=True)
