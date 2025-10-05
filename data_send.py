from pymongo import MongoClient
from datetime import datetime, timezone
import random, time
MONGO_URI="mongodb+srv://mayankrathore01092003_db_user:IFVPBwa6GAHVPQ3Y@cluster0.njqbdlh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client =MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db = client["icih46"]
telemetry_col = db["anomaliy"]
def send_test_data():
    data = {
 "sensor_id": "test_sensor",
 "temperature":round(random.uniform(10.0, 100.0), 2),
"vibration":round(random.uniform(0.0, 3.0), 3),
 "humidity" : round(random.uniform(20.0, 90.0), 2),
"current": round(random.uniform(10.0, 100.0), 2),
"timestamp": datetime.now(timezone.utc).isoformat()}
    telemetry_col.insert_one(data)
    print("Inserted:", data)
if __name__ == "__main__":
 while True:
        send_test_data()
        time.sleep(3)
