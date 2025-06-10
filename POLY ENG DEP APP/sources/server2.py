import os
from flask import Flask, jsonify, request, g , send_from_directory
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mactech',
    'database': 'poly_eng_app',
    'port': 3306
}

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploaded_files'
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
def upload_file():
    file = request.files.get('file')
    if file:
        try:
            # Save the file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Insert metadata into the database
            file_name = file.filename
            file_size = os.path.getsize(file_path)

            # Use the shared database connection
            g.cursor.execute(
                "INSERT INTO videos (vid_name, vid_size, path) VALUES (%s, %s, %s)",
                (file_name, file_size , file_path)
            )
            g.db.commit()

            return jsonify({'message': 'File uploaded and metadata saved successfully!', 'file': file_name}), 200
        except Exception as file_error:
            return jsonify({'message': f'Error saving file: {str(file_error)}'}), 500
    return jsonify({'message': 'No file uploaded!'}), 400

if __name__ == '__main__':
    app.run(debug=True)
