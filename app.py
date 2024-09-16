from flask import Flask, request, render_template, make_response
import mysql.connector
from mysql.connector import Error
import json
import csv
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Fetch database configuration from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_DATABASE = os.getenv('DB_DATABASE', 'skitdb')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            database=DB_DATABASE,
            user=DB_USER,
            password=DB_PASSWORD
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/regdata', methods=['GET', 'POST'])
def regdata():
    nm = request.args['name']
    em = request.args['email']
    pswd = request.args['pswd']
    ph = request.args['phone']

    connection = get_db_connection()
    if connection:
        sqlquery = f"INSERT INTO userdata1(name,email,pswd,phone) VALUES('{nm}','{em}','{pswd}','{ph}')"
        cursor = connection.cursor()
        cursor.execute(sqlquery)
        connection.commit()
        cursor.close()
        connection.close()
        msg = "Data Saved Successfully"
    else:
        msg = "Database connection failed"
    
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp

@app.route('/logdata', methods=['GET', 'POST'])
def logdata():
    em = request.args['email']
    pswd = request.args['pswd']

    connection = get_db_connection()
    if connection:
        sqlquery = f"SELECT COUNT(*) FROM userdata1 WHERE email='{em}' AND pswd='{pswd}'"
        cursor = connection.cursor()
        cursor.execute(sqlquery)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        msg = "Failure" if data[0][0] == 0 else "Success"
    else:
        msg = "Database connection failed"
    
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp

@app.route('/dashboard')
def dashboard():
    connection = get_db_connection()
    if connection:
        sqlquery = "SELECT COUNT(*) FROM dataset1 GROUP BY protocol_type"
        cursor = connection.cursor()
        cursor.execute(sqlquery)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('dashboard.html', icmpcount=data[0][0], tcpcount=data[1][0], udpcount=data[2][0])
    else:
        return "Database connection failed"

@app.route('/dataloader')
def dataloader():
    return render_template('dataloader.html')

@app.route('/savedataset1', methods=['POST'])
def savedataset1():
    if request.method == 'POST':
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()

            prod_mas = request.files['dt_file']
            filename = secure_filename(prod_mas.filename)
            prod_mas.save(os.path.join("./static/Uploads/", filename))

            fn = os.path.join("./static/Uploads/", filename)
            rows = []

            with open(fn, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    rows.append(row)
                    print(row)

            try:
                for row in rows[1:]:
                    if row[0][0] != "":
                        query = "INSERT INTO dataset1 VALUES (" + ",".join(f"'{col}'" for col in row) + ")"
                        print("query :" + query, flush=True)
                        cursor.execute(query)
                        connection.commit()
            except Exception as e:
                print(f"An exception occurred: {e}")
            csvfile.close()

            cursor.close()
            connection.close()
            return render_template('dataloader.html', data="Data loaded successfully")
        else:
            return "Database connection failed"

@app.route('/cleardataset', methods=['POST'])
def cleardataset():
    if request.method == 'POST':
        connection = get_db_connection()
        if connection:
            sqlquery = "DELETE FROM dataset1"
            print(sqlquery)
            cursor = connection.cursor()
            cursor.execute(sqlquery)
            connection.commit()
            cursor.close()
            connection.close()
            return render_template('dataloader.html', data="Data cleared successfully")
        else:
            return "Database connection failed"

@app.route('/planning')
def planning():
    connection = get_db_connection()
    if connection:
        sqlquery = "SELECT * FROM dataset1"
        print(sqlquery)
        cursor = connection.cursor()
        cursor.execute(sqlquery)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('planning.html', patdata=data)
    else:
        return "Database connection failed"

@app.route('/predict')
def predict():
    return render_template('prediction.html')

@app.route('/predictdata1', methods=['GET', 'POST'])
def predictdata1():
    protocol_type = request.args['protocol_type']
    service = request.args['service']
    flag = request.args['flag']
    src_bytes = request.args['src_bytes']
    dst_bytes = request.args['dst_bytes']
    dst_host_count = request.args['dst_host_count']

    connection = get_db_connection()
    if connection:
        sqlquery = f"SELECT class FROM dataset1 WHERE protocol_type='{protocol_type}' AND service='{service}' AND flag='{flag}' AND src_bytes='{src_bytes}' AND dst_bytes='{dst_bytes}' AND dst_host_count='{dst_host_count}' LIMIT 2"
        print(sqlquery)
        cursor = connection.cursor()
        cursor.execute(sqlquery)
        data = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()

        res = "Its Normal" if data[0][0] == "normal" else "Its Anomaly"
        msg = res
    else:
        msg = "Database connection failed"
    
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp

@app.route('/indexdata', methods=['GET', 'POST'])
def indexdata():
    fullname = request.args['fullname']
    emailaddr = request.args['emailaddr']
    phone = request.args['phone']
    subject = request.args['subject']

    connection = get_db_connection()
    if connection:
        sqlquery = f"INSERT INTO contactus(fullname,emailaddr,phone,subject) VALUES('{fullname}','{emailaddr}','{phone}','{subject}')"
        print(sqlquery)
        cursor = connection.cursor()
        cursor.execute(sqlquery)
        connection.commit()
        cursor.close()
        connection.close()
        msg = "Thank You For Your valuable Feedback!!"
    else:
        msg = "Database connection failed"
    
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True) 


