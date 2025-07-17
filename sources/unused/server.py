from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Flask route to fetch news data from the database
@app.route('/api/news', methods=['GET'])
def fetch_news():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="mactech",
            database="poly_eng_app",
            port=3306
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM news")
        news_list = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(news_list)
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/api/news2', methods=['GET'])
def fetch_news2():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="mactech",
            database="poly_eng_app",
            port=3306
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM news2")
        new_list = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(new_list)
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/api/zuva', methods=['GET'])
def fetch_zuva():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="mactech",
            database="poly_eng_app",
            port=3306
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM zuva")
        zuva_list = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(zuva_list)
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/api/files', methods=['GET'])
def fetch_notes():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="mactech",
            database="poly_eng_app",
            port=3306
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM files")
        files_list = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify(files_list)
    
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500




if __name__ == '__main__':
    app.run(debug=True, port=5000)
