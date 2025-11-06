import time
import adafruit_dht
import board

# --- Configurar el sensor (GPIO 4) ---
dht = adafruit_dht.DHT11(board.D4)

print("Leyendo DHT11 (Ctrl+C para salir)\n")

while True:
    try:
        temp = dht.temperature
        hum = dht.humidity
        if temp is not None and hum is not None:
            print(f"🌡  Temperatura: {temp:.1f} °C   💧 Humedad: {hum:.1f} %")
        else:
            print("Lectura inválida, reintentando...")
    except Exception as e:
        # Si falla una lectura, no detiene el programa
        print("Error:", e)
    time.sleep(2)