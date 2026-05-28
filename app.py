from flask import Flask, request, jsonify

import sqlite3

sensor_data_list = []

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        username TEXT,
        password TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id TEXT,
        temperature REAL,
        humidity REAL
    )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def home():
    return "IoT Platform Running Successfully"

@app.route('/register', methods=['POST'])
def register_device():

    data = request.get_json()

    device_id = data['device_id']
    username = data['username']
    password = data['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO devices (device_id, username, password)
    VALUES (?, ?, ?)
    ''', (device_id, username, password))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Device registered successfully"
    })

@app.route('/send_data', methods=['POST'])
def send_data():

    data = request.json

    device_id = data['device_id']
    temperature = data['temperature']
    humidity = data['humidity']

    print("Received Sensor Data:")
    print("Device ID:", device_id)
    print("Temperature:", temperature)
    print("Humidity:", humidity)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO sensor_data (device_id, temperature, humidity)VALUES (?, ?, ?)",
        (device_id, temperature, humidity)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Sensor data received successfully"
    })

@app.route('/get_data', methods=['GET'])
def get_data():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT device_id, temperature, humidity FROM sensor_data")

    rows = cursor.fetchall()

    conn.close()

    data = []

    for row in rows:
        data.append({
            "device_id": row[0],
            "temperature": row[1],
            "humidity": row[2]
        })

    return jsonify(data)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
