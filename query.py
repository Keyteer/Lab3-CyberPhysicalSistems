#!/usr/bin/env python3
import sqlite3
from datetime import datetime, timedelta, timezone

DB_PATH = "sensors.db"

def get_recent_readings(minutes=10):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    since = (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat()
    
    cur.execute("""
        SELECT sensor_id, ts, value 
        FROM reading 
        WHERE ts >= ? 
        ORDER BY ts DESC
    """, (since,))
    
    rows = cur.fetchall()
    conn.close()
    return rows

def get_minute_averages(minutes=10):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    since = (datetime.now(timezone.utc) - timedelta(minutes=minutes)).isoformat()
    
    cur.execute("""
        SELECT 
            sensor_id,
            strftime('%Y-%m-%d %H:%M:00', ts) as minute,
            AVG(value) as avg_value
        FROM reading 
        WHERE ts >= ?
        GROUP BY sensor_id, minute
        ORDER BY sensor_id, minute DESC
    """, (since,))
    
    rows = cur.fetchall()
    conn.close()
    return rows

def main():
    print("=== Últimas lecturas (10 minutos) ===")
    readings = get_recent_readings(10)
    for sensor, ts, value in readings:
        print(f"{sensor:12} {ts} -> {value:.2f}")
    
    print("\n=== Promedios por minuto (10 minutos) ===")
    averages = get_minute_averages(10)
    for sensor, minute, avg in averages:
        print(f"{sensor:12} {minute} -> {avg:.2f}")

if __name__ == "__main__":
    main()