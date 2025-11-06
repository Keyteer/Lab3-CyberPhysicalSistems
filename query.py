#!/usr/bin/env python3
import argparse
import sqlite3
from datetime import datetime, timedelta, timezone

DB_PATH = "sensors.db"

def get_recent_readings(minutes=10):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT MAX(ts) FROM reading")
    last_ts = cur.fetchone()[0]
    if not last_ts:
        conn.close()
        return []

    last_dt = datetime.fromisoformat(last_ts)
    since = (last_dt - timedelta(minutes=minutes)).isoformat()

    cur.execute(
        """
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
    cur.execute("SELECT MAX(ts) FROM reading")
    last_ts = cur.fetchone()[0]
    if not last_ts:
        conn.close()
        return []

    last_dt = datetime.fromisoformat(last_ts)
    since = (last_dt - timedelta(minutes=minutes)).isoformat()

    cur.execute(
        """
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--minutes", type=int, default=10, help="Número de minutos para consultar")
    args = parser.parse_args()
    print(f"=== Últimas lecturas ({args.minutes} minutos) ===")
    readings = get_recent_readings(args.minutes)
    for sensor, ts, value in readings:
        print(f"{sensor:12} {ts} -> {value:.2f}")
    
    print(f"\n=== Promedios por minuto ({args.minutes} minutos) ===")
    averages = get_minute_averages(args.minutes)
    for sensor, minute, avg in averages:
        print(f"{sensor:12} {minute} -> {avg:.2f}")

if __name__ == "__main__":
    main()