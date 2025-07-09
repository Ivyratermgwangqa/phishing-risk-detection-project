# synth_auth_logs.py
# Generate synthetic login records with anomalies
import random
import pandas as pd
from datetime import datetime, timedelta


def generate_logs(output_csv: str, days: int = 30):
    records = []
    # Define users, home loc, devices
    users = {'alice': (40.0, -74.0), 'bob': (34.0, -118.2)}
    devices = ['Laptop', 'Phone', 'Tablet']
    for d in range(days):
        for user, (lat, lon) in users.items():
            time = datetime.now().replace(hour=random.randint(8,17), minute=random.randint(0,59))
            loc = (lat + random.uniform(-0.1,0.1), lon + random.uniform(-0.1,0.1))
            device = random.choice(devices)
            records.append({'user': user, 'time': time, 'lat': loc[0], 'lon': loc[1], 'device': device, 'anomaly': False})
    # Inject example anomaly
    records.append({'user': 'alice', 'time': datetime.now(), 'lat': 48.8, 'lon': 2.3, 'device': 'Unknown', 'anomaly': True})
    pd.DataFrame(records).to_csv(output_csv, index=False)