#!/usr/bin/env python3
import os, time, sqlite3, random, argparse
from datetime import datetime, timezone

# --- Configuración ---
DB_PATH = "sensors.db"
SENSORS = [
    {"id": "dht11-temp", "type": "temperature"},
    {"id": "dht11-hum",  "type": "humidity"},
]

# Por defecto: usa hardware real, a menos que SIM=1
SIMULATION = os.environ.get("SIM", "0") == "1"

# --- Intentar usar el sensor  ---
try:
    import adafruit_dht
    import board
    dht_device = adafruit_dht.DHT11(board.D4)
except Exception as e:
    print("No se pudo inicializar DHT11, se usará modo simulación. Error:", e)
    SIMULATION = True

# --- Modo real (datos reales obtenidos del sensor) ---
def read_temp_hw():
    try:
        return dht_device.temperature
    except Exception as e:
        print(f"Error leyendo temperatura: {e}")
        return None

def read_hum_hw():
    try:
        return dht_device.humidity
    except Exception as e:
        print(f"Error leyendo humedad: {e}")
        return None

# --- Modo simulación (genera valores aleatorios) ---
def read_temp_sim():
    return 22.0 + random.uniform(-2.0, 2.0)  

def read_hum_sim():
    return 50.0 + random.uniform(-5.0, 5.0)  

def read_sensor(s):
    if s["type"] == "temperature":
        return read_temp_hw() if not SIMULATION else read_temp_sim()
    elif s["type"] == "humidity":
        return read_hum_hw() if not SIMULATION else read_hum_sim()
    return None

# --- Base de datos ---
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
        cur.execute("INSERT OR IGNORE INTO sensor(id, type) VALUES(?, ?)", (s["id"], s["type"]))
    conn.commit()

def insert_reading(conn, sensor_id, value):
    if value is not None:
        conn.execute("INSERT INTO reading(ts, sensor_id, value) VALUES (?, ?, ?)",
                     (datetime.now(timezone.utc).isoformat(), sensor_id, float(value)))
        conn.commit()

# --- main ---
def main(period=10.0, duration=600):
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    init_db(conn)
    t0 = time.time()

    print(f"Iniciando adquisición cada {period}s por {duration}s.")
    if SIMULATION:
        print("Modo simulación activado.\n")

    try:
        while time.time() - t0 < duration:
            for s in SENSORS:
                valor = read_sensor(s)
                if valor is not None:
                    insert_reading(conn, s["id"], valor)
                    print(f"{s['id']} -> {valor:.2f}")
                else:
                    print(f"No se pudo leer {s['id']}")
            time.sleep(period)
    except KeyboardInterrupt:
        print("\n Interrumpido por el usuario.")
    finally:
        conn.close()
        print("Base de datos cerrada correctamente.")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--period", type=float, default=10.0, help="Intervalo entre lecturas (segundos)")
    p.add_argument("--duration", type=int, default=600, help="Duración total de la adquisición (segundos)")
    args = p.parse_args()
    main(args.period, args.duration)
