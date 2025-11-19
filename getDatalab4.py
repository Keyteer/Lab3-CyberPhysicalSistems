#!/usr/bin/env python3
import os, time, sqlite3, random, argparse, statistics
from datetime import datetime, timezone

# ================================
# CONFIGURACIÓN GENERAL
# ================================
DB_PATH = "sensors.db"
DIAG_LOG = "diagnostics.log"
WINDOW_MINUTES = 5          # ventana temporal de 5 min
UMBRAL_FACTOR = 2.5         # k veces la desviación estándar
SMART_ERROR_LIMIT = 3       # cuántas anomalías consecutivas
NORMAL_PERIOD = 10          # periodo normal
FAST_PERIOD = 4             # periodo rápido

SENSORS = [
    {"id": "dht11-temp", "type": "temperature"},
    {"id": "dht11-hum",  "type": "humidity"},
]

SIMULATION = os.environ.get("SIM", "0") == "1"

# ================================
# SENSOR REAL O SIMULADO
# ================================
try:
    import adafruit_dht
    import board
    dht_device = adafruit_dht.DHT11(board.D4)
except Exception:
    print("[INFO] No se pudo iniciar DHT11 → MODO SIMULACIÓN")
    SIMULATION = True

def read_temp_hw():
    try:
        return dht_device.temperature
    except:
        return None

def read_hum_hw():
    try:
        return dht_device.humidity
    except:
        return None

def read_temp_sim():
    return 22 + random.uniform(-2, 2)

def read_hum_sim():
    return 50 + random.uniform(-5, 5)

def read_sensor(s):
    if s["type"] == "temperature":
        return read_temp_hw() if not SIMULATION else read_temp_sim()
    elif s["type"] == "humidity":
        return read_hum_hw() if not SIMULATION else read_hum_sim()
    return None

# ================================
# BASE DE DATOS
# ================================
def init_db(conn):
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS sensor(
        id TEXT PRIMARY KEY,
        type TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS reading(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        sensor_id TEXT NOT NULL,
        value REAL NOT NULL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS diagnostics(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT,
        sensor_id TEXT,
        value REAL,
        mean REAL,
        median REAL,
        std REAL,
        n INTEGER,
        error REAL,
        threshold REAL,
        result TEXT
    )""")

    for s in SENSORS:
        cur.execute("INSERT OR IGNORE INTO sensor(id, type) VALUES(?, ?)", (s["id"], s["type"]))

    conn.commit()

def insert_reading(conn, sensor_id, value):
    conn.execute("INSERT INTO reading(ts, sensor_id, value) VALUES (?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(), sensor_id, float(value)))
    conn.commit()

# ================================
# CÁLCULO ESTADÍSTICAS EN VENTANA
# ================================
def get_window_stats(conn, sensor_id, minutes=WINDOW_MINUTES):
    cur = conn.cursor()
    cur.execute("""
        SELECT value FROM reading
        WHERE sensor_id = ? 
          AND ts >= datetime('now', ?)
        ORDER BY ts DESC
    """, (sensor_id, f"-{minutes} minutes"))

    rows = [r[0] for r in cur.fetchall()]

    if len(rows) == 0:
        return None

    mean = statistics.mean(rows)
    median = statistics.median(rows)
    std = statistics.stdev(rows) if len(rows) > 1 else 0.0

    return {
        "mean": mean,
        "median": median,
        "std": std,
        "n": len(rows),
        "values": rows
    }

# ================================
# DIAGNÓSTICO AUTOMÁTICO
# ================================
def generar_diagnostico(conn, sensor_id, valor):
    stats = get_window_stats(conn, sensor_id)

    if stats is None or stats["n"] < 2:
        return None  # no hay datos suficientes aún

    mean = stats["mean"]
    median = stats["median"]
    std = stats["std"]
    n = stats["n"]

    error = abs(valor - mean)
    umbral = UMBRAL_FACTOR * std

    if std == 0:
        result = "OK"
    else:
        if error > umbral:
            result = "ANOMALIA"
        elif error > std:
            result = "ADVERTENCIA"
        else:
            result = "OK"

    ts_now = datetime.now(timezone.utc).isoformat()

    conn.execute(
        """INSERT INTO diagnostics(ts, sensor_id, value, mean, median, std, n, error, threshold, result)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (ts_now, sensor_id, valor, mean, median, std, n, error, umbral, result)
    )
    conn.commit()

    # opcional: guardar también en archivo
    with open(DIAG_LOG, "a") as f:
        f.write(f"{ts_now} | {sensor_id} | val={valor:.2f} | mean={mean:.2f} | "
                f"std={std:.2f} | err={error:.2f} | umbral={umbral:.2f} | {result}\n")

    return result

# ================================
# MAIN LOOP + SMART VALIDATION
# ================================
def main(period=10, duration=600):
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    init_db(conn)

    print(f"[INFO] Adquisición cada {period}s durante {duration}s")

    t0 = time.time()
    anomaly_count = 0
    current_period = period

    try:
        while time.time() - t0 < duration:

            for s in SENSORS:
                value = read_sensor(s)

                if value is None:
                    print(f"[ERROR] No se pudo leer {s['id']}")
                    continue

                insert_reading(conn, s["id"], value)
                print(f"[DATA] {s['id']} = {value:.2f}")

                result = generar_diagnostico(conn, s["id"], value)

                # SMART VALIDATION
                if result == "ANOMALIA":
                    anomaly_count += 1
                else:
                    anomaly_count = 0  # se resetea si vuelve a normalidad

                # Cambiar frecuencia
                if anomaly_count >= SMART_ERROR_LIMIT:
                    current_period = FAST_PERIOD
                else:
                    current_period = NORMAL_PERIOD

            time.sleep(current_period)

    except KeyboardInterrupt:
        print("\n[INFO] Interrumpido por usuario.")
    finally:
        conn.close()
        print("[INFO] Base de datos cerrada.")

# ================================
# ARGUMENTOS CLI
# ================================
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--period", type=float, default=10, help="Periodo inicial de muestreo")
    p.add_argument("--duration", type=int, default=600, help="Duración en segundos")
    args = p.parse_args()
    main(args.period, args.duration)
