#!/usr/bin/env python3

import sqlite3
import time
from datetime import datetime
import argparse

# Librerías del sensor 
import adafruit_dht
import board

# Base de datos donde se guardan los datos
DB_PATH = "sensors.db"

# Se configura el pin donde está conectado el DHT11
dht = adafruit_dht.DHT11(board.D4)

# Función para leer los valores del sensor
def leer_sensor():
    try:
        temperatura = dht.temperature
        humedad = dht.humidity
        return temperatura, humedad
    except Exception as e:
        print("Error al leer el sensor:", e)
        return None, None

# Función para crear la tabla si no existe
def crear_tabla(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            sensor TEXT NOT NULL,
            value REAL NOT NULL
        )
    """)
    conn.commit()

# Función para guardar los datos
def guardar_dato(conn, tipo, valor):
    hora = datetime.utcnow().isoformat()
    conn.execute(
        "INSERT INTO readings(ts, sensor, value) VALUES (?, ?, ?)",
        (hora, tipo, valor)
    )
    conn.commit()


def main(periodo=10.0, duracion=600):
    conn = sqlite3.connect(DB_PATH)
    crear_tabla(conn)
    inicio = time.time()

    print("Iniciando lectura de datos...")
    print(f"Se guardarán datos cada {periodo} segundos durante {duracion} segundos.\n")

    try:
        while time.time() - inicio < duracion:
            temp, hum = leer_sensor()
            if temp is not None and hum is not None:
                guardar_dato(conn, "temperature", temp)
                guardar_dato(conn, "humidity", hum)
                print(f"Temperatura: {temp:.1f} °C  |  Humedad: {hum:.1f} %")
            else:
                print("No se pudo leer el sensor en este intento.")
            time.sleep(periodo)
    except KeyboardInterrupt:
        print("\nLectura interrumpida por el usuario.")
    finally:
        conn.close()
        print("Conexión cerrada y datos guardados en la base de datos.")

# Permite pasar los parámetros desde la terminal
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lectura de temperatura y humedad con DHT11")
    parser.add_argument("--period", type=float, default=10.0, help="Cada cuántos segundos leer el sensor (por defecto 10s)")
    parser.add_argument("--duration", type=int, default=600, help="Cuánto tiempo leer datos (por defecto 10 minutos)")
    args = parser.parse_args()
    main(args.period, args.duration)
