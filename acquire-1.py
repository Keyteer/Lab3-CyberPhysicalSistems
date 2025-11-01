#!/usr/bin/env python3
import os, time, sqlite3, random, argparse
from datetime import datetime

# --- Config ---
DB_PATH = "cps.db"
SENSORS = [
    {"id": "temp-1", "type": "temperature"},
    {"id": "vib-1",  "type": "vibration"},
]
SIMULATION = os.environ.get("SIM", "1") == "1"   # SIM=0 para usar HW real

# --- HW opcional (ejemplo DS18B20 / MPU6050) ---
def read_temp_hw():
    # TODO: implementar lectura real (1-Wire). Plantilla de retorno:
    return 20.0 + random.uniform(-0.3, 0.3)

def read_vib_hw():
    # TODO: implementar lectura real (I2C). Plantilla de retorno (RMS m/s^2):
    return 0.08 + random.uniform(0, 0.05)

def read_temp_sim(): return 22.0 + 2.0*random.random()
def read_vib_sim():  return 0.1  + 0.1*random.random()

def read_sensor(s):
    if s["type"] == "temperature":
        return read_temp_hw() if not SIMULATION else read_temp_sim()
    if s["type"] == "vibration":
        return read_vib_hw() if not SIMULATION else read_vib_sim()
    return None

# --- DB ---
def init_db(conn):
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS sensor(
        id TEXT PRIMARY KEY, type TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS reading(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        sensor_id TEXT NOT NULL,
        value REAL NOT NULL,
        FOREIGN KEY(sensor_id) REFERENCES sensor(id))""")
    cur.execute("CREATE INDEX IF NOT EXISTS ix_reading_sensor_ts ON reading(sensor_id, ts)")
    for s in SENSORS:
        cur.execute("INSERT OR IGNORE INTO sensor(id,type) VALUES(?,?)",(s["id"], s["type"]))
    conn.commit()

def insert_reading(conn, sensor_id, value):
    conn.execute("INSERT INTO reading(ts,sensor_id,value) VALUES(?,?,?)",
                 (datetime.utcnow().isoformat(), sensor_id, float(value)))
    conn.commit()

def main(period=1.0, duration=300):
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    init_db(conn)
    t0 = time.time()
    while time.time() - t0 < duration:
        for s in SENSORS:
            v = read_sensor(s)
            insert_reading(conn, s["id"], v)
            print(f"{s['id']} -> {v:.3f}")
        time.sleep(period)
    conn.close()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--period", type=float, default=1.0)
    p.add_argument("--duration", type=int, default=300)
    args = p.parse_args()
    main(args.period, args.duration)
