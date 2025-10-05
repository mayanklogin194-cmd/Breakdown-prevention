from flask import Flask, render_template, jsonify
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta
import threading
import time

app = Flask(__name__)

# MongoDB setup
u = "mongodb+srv://mayankrathore01092003_db_user:IFVPBwa6GAHVPQ3Y@cluster0.njqbdlh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(u)
db = client["icih46"]
dATA = db["anomaliy"]


# Anomaly checking function
def check_anomalies(record):
    an = []
    if record.get("temperature") is not None and record["temperature"] > 70:
        an.append(f"temperature={record['temperature']} > 70")
    if record.get("humidity") is not None and record["humidity"] > 80:
        an.append(f"humidity={record['humidity']} > 80")
    if record.get("vibration") is not None and record["vibration"] > 2:
        an.append(f"vibration={record['vibration']} > 2")
    if record.get("current") is not None and record["current"] > 50:
        an.append(f"current={record['current']} > 50")
    return an


# Fetch recent data
def fetch_recent_data(seconds=20):
    now = datetime.now(timezone.utc)
    past = now - timedelta(seconds=seconds)
    records = list(dATA.find(
        {"timestamp": {"$gte": past.isoformat()}},
        sort=[("timestamp", 1)]
    ).limit(1000))

    processed = []
    for rec in records:
        rec["_id"] = str(rec["_id"])
        anomalies = check_anomalies(rec)
        is_anomaly = len(anomalies) > 0
        processed.append({
            "timestamp": rec["timestamp"],
            "temperature": rec.get("temperature", 0),
            "vibration": rec.get("vibration", 0),
            "humidity": rec.get("humidity", 0),
            "current": rec.get("current", 0),
            "is_anomaly": is_anomaly,
            "anomalies": anomalies if is_anomaly else []
        })
    return processed


# Anomaly detector thread
def anomaly_detector_thread():
    while True:
        now = datetime.now(timezone.utc)
        ten_sec_ago = now - timedelta(seconds=10)
        latest_records = dATA.find({"timestamp": {"$gte": ten_sec_ago.isoformat()}})

        new_data_logged = False
        for rec in latest_records:
            new_data_logged = True
            anomalies = check_anomalies(rec)
            if anomalies:
                print(f"Anomaly Logged: {rec['sensor_id']} at {rec['timestamp']}: {anomalies}")
        time.sleep(10)


# Routes
@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/api/data')
def api_data():
    data = fetch_recent_data(seconds=20)
    return jsonify(data)


if __name__ == '__main__':
    anomaly_thread = threading.Thread(target=anomaly_detector_thread, daemon=True)
    anomaly_thread.start()
    print("Anomaly Detector Thread Started")
    print("Dashboard Webserver Starting")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
