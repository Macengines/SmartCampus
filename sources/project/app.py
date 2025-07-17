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
UPLOAD_FOLDER = 'uploads'
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

@app.route('/api/store_student', methods=['POST'])
def store_student():
    try:
        data = request.get_json()

        # Extract fields from JSON
        fname = data.get("NAME")
        sname = data.get("SURNAME")
        sid = data.get("STUDENT ID")
        dept = data.get("DEPARTMENT")
        course = data.get("COURSE")
        level = data.get("LEVEL")

        # Validate
        if not all([fname, sname, sid, dept, course, level]):
            return jsonify({"message": "Missing fields"}), 400

        # Insert into database
        g.cursor.execute("""
            INSERT INTO students (name, surname, student_id, department, course, level)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (fname, sname, sid, dept, course, level))
        g.db.commit()

        return jsonify({"message": "Student details saved successfully!"}), 200

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@app.route('/api/update_level', methods=['POST'])
def update_level():
    try:
        if os.path.exists("students.json"):
                with open("students.json", "r") as f:
                    data = json.load(f)

                # Handle both list and dictionary cases
                if isinstance(data, list):  # If it's a list, fetch the first student
                    student = data[0] if data else {}
                elif isinstance(data, dict):  # If it's a dictionary, use it directly
                    student = data
                else:
                    student = {}
        level = student.get("LEVEL", "")
        student_id = student.get("STUDENT ID", "")
        

        # update into database
        sql = """
            UPDATE students SET level = %s WHERE student_id=%s
        """
        g.cursor.execute(sql,(level,student_id))
        g.db.commit()

        return jsonify({"message": "Student details saved successfully!"}), 200

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

#posting to the db
@app.route('/api/upload_file', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        try:
            if os.path.exists("students.json"):
                with open("students.json", "r") as f:
                    data = json.load(f)

                # Handle both list and dictionary cases
                if isinstance(data, list):  # If it's a list, fetch the first student
                    student = data[0] if data else {}
                elif isinstance(data, dict):  # If it's a dictionary, use it directly
                    student = data
                else:
                    student = {}
            
            department = student.get("DEPARTMENT", "")
            course_name = student.get("COURSE", "")
            level = student.get("LEVEL", "")
            content_type = "note"
            # Save the file
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Insert metadata into the database
            file_name = file.filename
            file_size = os.path.getsize(file_path)
            file_type = os.path.splitext(file_name)[1]  # Extract the file extension
            file_name_without_extension = os.path.splitext(file_name)[0]
            # Use the shared database connection
            g.cursor.execute(
                "INSERT INTO contents (file_name, file_size, department, course, level, content_type) VALUES (%s, %s, %s, %s, %s, %s)",  # Include `type`
                (file_name_without_extension, file_size, department,course_name,level, file_type)  # Add `file_type` as a value
            )
            g.db.commit()

            return jsonify({'message': 'File uploaded and metadata saved successfully!', 'file': file_name}), 200
        except Exception as file_error:
            return jsonify({'message': f'Error saving file: {str(file_error)}'}), 500
    return jsonify({'message': 'No file uploaded!'}), 400



# getting from the db
@app.route('/api/files', methods=['GET'])
def get_files():

    
    with open("students.json", "r") as file:
        details = json.load(file)
        dept = details.get("DEPARTMENT", "")
        course = details.get("COURSE", "")
        level = details.get("LEVEL", "")
        
    
    sql = """
        SELECT * FROM contents
        WHERE department = %s AND course = %s AND level = %s AND content_type = "note"
    """
    g.cursor.execute(sql,(dept,course,level))

    files_list = g.cursor.fetchall()
    g.cursor.close()

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
