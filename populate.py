import time
import sqlite3
from datetime import datetime
import random

# Pseudocode function to get sensor data
def read_sensors():
    # Return a dict or tuple with your sensor readings
    return {
        'timestamp': datetime.now(),
        'temperature': random.random()*20,
        'humidity': random.random()*100,
        'pressure': random.random()*1000,
        'wind_speed': random.random()*20,
        'wind_direction': random.random()*360,
        'rainfall': random.random()*30
    }

def main():
    buffer = []
    db_path = './measurements.db'
    last_write = time.time()
    write_interval = 300  # 5 minutes

    # while True:
    for _ in range(100):
        data = read_sensors()
        buffer.append(data)

        # Bulk-insert if write interval has passed
        # if (time.time() - last_write) > write_interval:
        write_to_db(db_path, buffer)
        buffer = []  # clear the in-memory buffer
        last_write = time.time()

    # time.sleep(10)  # measure every 10s

def write_to_db(db_path, buffer):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Make sure table exists
    c.execute('''CREATE TABLE IF NOT EXISTS measurements (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      timestamp DATETIME NOT NULL,
      temperature REAL,
      humidity REAL,
      pressure REAL,
      wind_speed REAL,
      wind_direction REAL,
      rainfall REAL
    );''')

    # Bulk-insert
    insert_query = '''INSERT INTO measurements
        (timestamp, temperature, humidity, pressure, wind_speed, wind_direction, rainfall)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    '''
    c.executemany(
        insert_query,
        [
            (
                entry['timestamp'].isoformat(),
                entry['temperature'],
                entry['humidity'],
                entry['pressure'],
                entry['wind_speed'],
                entry['wind_direction'],
                entry['rainfall']
            ) for entry in buffer
        ]
    )

    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
