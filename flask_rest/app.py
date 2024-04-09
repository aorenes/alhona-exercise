import os
import psycopg2
from flask import Flask, render_template 

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='35.205.205.14',
                            database='mqtt',
                            user='alhona',
                            password='alhona')
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM payload;')
    payloads = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', payloads=payloads)
