#!/usr/bin/env python3
import sqlite3, time, random, argparse
from datetime import datetime


DB_PATH = "sensors.db"
SIMULATION = True  # True para simular lecturas, False si usas hardware real

# --- Lectura del sensor ---
def read_sensor():
    """
    Simula la lectura de un sensor de temperatura/humedad.
    En una Raspberry real podrías usar adafruit_dht o gpiozero.
    """
    if SIMULATION:
        temp = 22.0 + random.uniform(-1.5, 1.5)
        hum = 50.0 + random.uniform(-5, 5)
    else:
        # Ejemplo para sensor DHT11 real:
        # dht = adafruit_dht.DHT11(board.D4)
        # temp = dht.temperature
        # hum = dht.humidity
        temp, hum = None, None
    return temp, hum

# --- Base de datos ---
def init_db(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            sensor TEXT NOT NULL,
            value REAL NOT NULL
        )
    """)
    conn.commit()

def insert_reading(conn, sensor, value):
    conn.execute(
        "INSERT INTO readings(ts, sensor, value) VALUES(?,?,?)",
        (datetime.utcnow().isoformat(), sensor, float(value))
    )
    conn.commit()

# --- Bucle principal ---
def main(period=10.0, duration=600):
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    t0 = time.time()

    print(f"[INFO] Adquisición iniciada. Guardando datos cada {period}s por {duration}s.")

    try:
        while time.time() - t0 < duration:
            temp, hum = read_sensor()
            if temp is not None and hum is not None:
                insert_reading(conn, "temperature", temp)
                insert_reading(conn, "humidity", hum)
                print(f"Temp: {temp:.1f} °C | Hum: {hum:.1f} %")
            else:
                print("[WARN] Lectura inválida, se omite muestra.")
            time.sleep(period)
    except KeyboardInterrupt:
        print("\n[INFO] Adquisición interrumpida por el usuario.")
    finally:
        conn.close()
        print("[INFO] Base de datos cerrada correctamente.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adquisición de temperatura y humedad")
    parser.add_argument("--period", type=float, default=10.0, help="Periodo de muestreo (s)")
    parser.add_argument("--duration", type=int, default=600, help="Duración total (s)")
    args = parser.parse_args()
    main(args.period, args.duration)
