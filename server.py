from flask import Flask, jsonify, request, send_from_directory
import sqlite3
import os

app = Flask(__name__)

DB_PATH = '/home/aart/measurements/measurements.db'
if "DEBUG_WEATHER_DB" in os.environ:
    DB_PATH = os.environ["DEBUG_WEATHER_DB"]

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

@app.route('/api/measurements', methods=['GET'])
def get_measurements():
    start = request.args.get('start')
    end = request.args.get('end')

    conn = get_db_connection()
    c = conn.cursor()

    query = "SELECT * FROM measurements ORDER BY timestamp DESC LIMIT 10000"
    params = []

    if start and end:
        query += " WHERE timestamp BETWEEN ? AND ?"
        params = [start, end]

    c.execute(query, params)
    rows = c.fetchall()
    conn.close()

    # Convert rows to a list of dict
    data = [dict(row) for row in rows]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
