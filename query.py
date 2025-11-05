#!/usr/bin/env python3

import sqlite3
from datetime import datetime, timedelta

# Nombre del archivo de base de datos
DB_PATH = "sensors.db"

# Función para mostrar las lecturas de los últimos 10 minutos
def mostrar_lecturas_recientes(conn):
    tiempo_limite = datetime.utcnow() - timedelta(minutes=10)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ts, sensor, value
        FROM readings
        WHERE ts >= ?
        ORDER BY ts DESC
    """, (tiempo_limite.isoformat(),))

    filas = cursor.fetchall()

    print("\n--- Lecturas de los últimos 10 minutos ---")
    if len(filas) == 0:
        print("No hay datos en los últimos 10 minutos.")
    else:
        for fila in filas:
            fecha, tipo, valor = fila
            if tipo == "temperature":
                unidad = "°C"
            else:
                unidad = "%"
            print(f"{fecha} | {tipo} | {valor:.1f} {unidad}")

# Función para mostrar el promedio por minuto
def mostrar_promedios_por_minuto(conn):
    tiempo_limite = datetime.utcnow() - timedelta(minutes=10)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT substr(ts, 1, 16) AS minuto, sensor, AVG(value)
        FROM readings
        WHERE ts >= ?
        GROUP BY minuto, sensor
        ORDER BY minuto DESC
    """, (tiempo_limite.isoformat(),))

    filas = cursor.fetchall()

    print("\n--- Promedio por minuto (últimos 10 minutos) ---")
    if len(filas) == 0:
        print("No hay datos para calcular promedios.")
    else:
        for fila in filas:
            minuto, tipo, promedio = fila
            if tipo == "temperature":
                unidad = "°C"
            else:
                unidad = "%"
            print(f"{minuto} | {tipo} | {promedio:.1f} {unidad}")

# Programa principal
def main():
    try:
        conn = sqlite3.connect(DB_PATH)
        mostrar_lecturas_recientes(conn)
        mostrar_promedios_por_minuto(conn)
    except Exception as e:
        print("Error al consultar la base de datos:", e)
    finally:
        conn.close()
        print("\nConexión cerrada.")

if __name__ == "__main__":
    main()
