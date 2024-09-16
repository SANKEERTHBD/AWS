from flask import Flask, request, render_template, make_response
import mysql.connector
from mysql.connector import Error
import json
import csv
import os
from werkzeug.utils import secure_filename
# for linking flask and angular
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


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
    # Data gathering
    nm = request.args['name']
    em = request.args['email']
    pswd = request.args['pswd']
    ph = request.args['phone']

    # Data transmission to db
    connection = mysql.connector.connect(
        host='localhost',  # Since MySQL is on the same machine
        database='skitdb',
        user='root',
        password=''
    )
    sqlquery = f"insert into userdata1(name,email,pswd,phone) values('{nm}','{em}','{pswd}','{ph}')"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    connection.commit()
    connection.close()
    cursor.close()
    msg = "Data Saved Successfully"
    resp = make_response(json.dumps(msg))

    print(msg, flush=True)
    return resp


@app.route('/logdata', methods=['GET', 'POST'])
def logdata():
    # Data gathering
    em = request.args['email']
    pswd = request.args['pswd']

    # Data transmission to db
    connection = mysql.connector.connect(
        host='localhost',  # Since MySQL is on the same machine
        database='skitdb',
        user='root',
        password=''
    )
    sqlquery = f"select count(*) from userdata1 where email='{em}' and pswd='{pswd}'"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    connection.close()
    cursor.close()
    msg = "Failure" if data[0][0] == 0 else "Success"

    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


@app.route('/dashboard')
def dashboard():
    connection = mysql.connector.connect(
        host='localhost',  # Since MySQL is on the same machine
        database='skitdb',
        user='root',
        password=''
    )
    sqlquery = "select count(*) from dataset1 group by protocol_type"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    connection.close()
    cursor.close()
    return render_template('dashboard.html', icmpcount=data[0][0], tcpcount=data[1][0], udpcount=data[2][0])


@app.route('/dataloader')
def dataloader():
    return render_template('dataloader.html')


@app.route('/savedataset1', methods=['POST'])
def savedataset1():
    print("request :" + str(request), flush=True)
    if request.method == 'POST':
        connection = mysql.connector.connect(
            host='localhost',  # Since MySQL is on the same machine
            database='skitdb',
            user='root',
            password=''
        )
        cursor = connection.cursor()

        prod_mas = request.files['dt_file']
        filename = secure_filename(prod_mas.filename)
        prod_mas.save(os.path.join("./static/Uploads/", filename))

        # csv reader
        fn = os.path.join("./static/Uploads/", filename)

        # initializing the titles and rows list
        rows = []

        with open(fn, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows.append(row)
                print(row)

        try:
            for row in rows[1:]:
                if row[0][0] != "":
                    query = "insert into dataset1 values (" + ",".join(f"'{col}'" for col in row) + ")"
                    print("query :" + query, flush=True)
                    cursor.execute(query)
                    connection.commit()
        except Exception as e:
            print(f"An exception occurred: {e}")
        csvfile.close()

        connection.close()
        cursor.close()
        return render_template('dataloader.html', data="Data loaded successfully")


@app.route('/cleardataset', methods=['POST'])
def cleardataset():
    print("request :" + str(request), flush=True)
    if request.method == 'POST':
        connection = mysql.connector.connect(
            host='localhost',  # Since MySQL is on the same machine
            database='skitdb',
            user='root',
            password=''
        )
        sqlquery = "delete from dataset1"
        print(sqlquery)
        cursor = connection.cursor()
        cursor.execute(sqlquery)
        connection.commit()
        connection.close()
        cursor.close()
        return render_template('dataloader.html', data="Data cleared successfully")


@app.route('/planning')
def planning():
    connection = mysql.connector.connect(
        host='localhost',  # Since MySQL is on the same machine
        database='skitdb',
        user='root',
        password=''
    )
    sqlquery = "select * from dataset1"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    connection.close()
    cursor.close()
    return render_template('planning.html', patdata=data)


@app.route('/predict')
def predict():
    return render_template('prediction.html')


@app.route('/predictdata1', methods=['GET', 'POST'])
def predictdata1():
    # Data gathering
    protocol_type = request.args['protocol_type']
    service = request.args['service']
    flag = request.args['flag']
    src_bytes = request.args['src_bytes']
    dst_bytes = request.args['dst_bytes']
    dst_host_count = request.args['dst_host_count']

    # Data transmission to db
    connection = mysql.connector.connect(
        host='localhost',  # Since MySQL is on the same machine
        database='skitdb',
        user='root',
        password=''
    )
    sqlquery = f"select class from dataset1 where protocol_type='{protocol_type}' and service='{service}' and flag='{flag}' and src_bytes='{src_bytes}' and dst_bytes='{dst_bytes}' and dst_host_count='{dst_host_count}' limit 2"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    data = cursor.fetchall()
    connection.commit()
    connection.close()
    cursor.close()

    # Data prediction
    res = "Its Normal" if data[0][0] == "normal" else "Its Anomaly"
    msg = res
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


@app.route('/indexdata', methods=['GET', 'POST'])
def indexdata():
    # Data gathering
    fullname = request.args['fullname']
    emailaddr = request.args['emailaddr']
    phone = request.args['phone']
    subject = request.args['subject']

    # Data transmission to db
    connection = mysql.connector.connect(
        host='localhost',  # Since MySQL is on the same machine
        database='skitdb',
        user='root',
        password=''
    )
    sqlquery = f"insert into contactus(fullname,emailaddr,phone,subject) values('{fullname}','{emailaddr}','{phone}','{subject}')"
    print(sqlquery)
    cursor = connection.cursor()
    cursor.execute(sqlquery)
    connection.commit()
    connection.close()
    cursor.close()
    msg = "Thank You For Your valuable Feedback!!"
    resp = make_response(json.dumps(msg))
    print(msg, flush=True)
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
