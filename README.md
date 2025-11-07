# Smart sensor and logger on Raspberry Pi Enviroment

## Members:

- María Castillo
- Pedro Palacios
- Franco Vidal

## Description
Este proyecto consiste en la implementación de un sistema básico de adquisición y consulta de los datos humedad relativa y temperatura a través de un sensor DHT11 conectado a una Raspberry Pi. Los datos junto con su timestap se guardan en una base de datos mediante la librería sqlite3 y se genera el archivo sensors.db.
El sistema cuenta, con dos modos (simulación y real), el modo simulación genera valores aleatorios para los parámetros temperatura y humedad dentro de los rangos establecidos en el programa, dicho modo se puede activar al inicio de modo manual y además se usa en reemplazo del modo real cuando falla. El modo real lee los datos de humedad y tiempo directamente desde el sensor DHT11 mediante la librería `adafruit_dht`. Además, se garantiza el sistema garantiza que al ocurrir interrupciones los datos se guarden de todas formas sin interrumpir el programa.

Funciones de los archivos del sistema:

1. **`getData.py`**
   - Por defecto al ejecutar se activa el modo real (uso del HW).   
   - Lee los datos del sensor DHT11 cada cierto intervalo (por defecto cada 10 segundos).  
   - Guarda los datos en la base de datos (sensors.db).  
   - Si ocurre un error de lectura, el programa no se detiene.  
   - Si no se detecta el sensor, entra en modo simulación.

2. **`query.py`**  
   - Consulta los datos guardados en la base de datos (sensors.db).  
   - Muestra las lecturas (temperatura y humedad) de los últimos minutos (por defecto 10) en orden descendente en función de su timestap.  
   - Calcula el promedio por minuto de los valores para la temperatura y humedad. 


## Usage:

```
usage: getData.py [-h] [--period PERIOD] [--duration DURATION]

options:
  -h, --help           show this help message and exit
  --period PERIOD      Intervalo entre lecturas (segundos)
  --duration DURATION  Duración total de la adquisición (segundos)
```

```
usage: query.py [-h] [--minutes MINUTES]

options:
  -h, --help         show this help message and exit
  --minutes MINUTES  Número de minutos para consultar
```


## Execution examples:
```console
$ python getData.py --duration 60
Iniciando adquisición cada 10.0s por 60s.
dht11-temp -> 21.80
dht11-hum -> 53.00
dht11-temp -> 21.80
dht11-hum -> 53.00
dht11-temp -> 21.80
dht11-hum -> 53.00
dht11-temp -> 21.80
dht11-hum -> 53.00
^Creceived SIGINT


Interrumpido por el usuario.
Base de datos cerrada correctamente.
```

```console
$ python query.py 
=== Últimas lecturas (10 minutos) ===
dht11-hum    2025-11-06T22:06:34.566254+00:00 -> 53.00
dht11-temp   2025-11-06T22:06:34.556310+00:00 -> 21.70
dht11-hum    2025-11-06T22:06:24.286486+00:00 -> 53.00
dht11-temp   2025-11-06T22:06:24.274083+00:00 -> 21.70
dht11-hum    2025-11-06T22:06:14.008564+00:00 -> 53.00
dht11-temp   2025-11-06T22:06:13.995711+00:00 -> 21.70
dht11-hum    2025-11-06T22:06:03.726969+00:00 -> 53.00
dht11-temp   2025-11-06T22:06:03.715072+00:00 -> 21.70
dht11-hum    2025-11-06T22:05:53.449535+00:00 -> 53.00
dht11-temp   2025-11-06T22:05:53.435738+00:00 -> 21.70
dht11-hum    2025-11-06T22:05:43.170116+00:00 -> 53.00
dht11-temp   2025-11-06T22:05:43.159843+00:00 -> 21.70
dht11-hum    2025-11-06T22:05:32.888750+00:00 -> 53.00
dht11-hum    2025-11-06T22:05:22.622641+00:00 -> 53.00
dht11-temp   2025-11-06T22:05:22.611864+00:00 -> 21.70
dht11-hum    2025-11-06T22:05:12.344230+00:00 -> 53.00
dht11-temp   2025-11-06T22:05:12.329410+00:00 -> 21.70
dht11-hum    2025-11-06T22:05:02.060936+00:00 -> 53.00
dht11-temp   2025-11-06T22:05:02.051303+00:00 -> 21.70
dht11-hum    2025-11-06T22:04:51.786043+00:00 -> 53.00
dht11-temp   2025-11-06T22:04:51.775178+00:00 -> 21.70
dht11-hum    2025-11-06T22:04:41.504584+00:00 -> 53.00
dht11-temp   2025-11-06T22:04:41.495142+00:00 -> 21.70
dht11-hum    2025-11-06T22:04:31.219774+00:00 -> 54.00
dht11-temp   2025-11-06T22:04:31.209735+00:00 -> 21.70
dht11-hum    2025-11-06T22:04:20.940616+00:00 -> 54.00
dht11-temp   2025-11-06T22:04:20.929471+00:00 -> 21.70
dht11-hum    2025-11-06T22:04:10.660729+00:00 -> 54.00
dht11-temp   2025-11-06T22:04:10.650335+00:00 -> 21.70
dht11-hum    2025-11-06T22:04:00.379260+00:00 -> 54.00
dht11-hum    2025-11-06T22:03:50.110570+00:00 -> 54.00
dht11-temp   2025-11-06T22:03:50.099138+00:00 -> 21.70
dht11-hum    2025-11-06T22:03:39.827967+00:00 -> 54.00
dht11-temp   2025-11-06T22:03:39.818288+00:00 -> 21.70
dht11-hum    2025-11-06T22:03:29.552032+00:00 -> 54.00
dht11-temp   2025-11-06T22:03:29.541484+00:00 -> 21.70
dht11-hum    2025-11-06T22:03:19.272442+00:00 -> 54.00
dht11-temp   2025-11-06T22:03:19.262753+00:00 -> 21.70
dht11-hum    2025-11-06T22:03:08.992369+00:00 -> 54.00
dht11-temp   2025-11-06T22:03:08.981710+00:00 -> 21.70
dht11-hum    2025-11-06T22:02:58.715211+00:00 -> 54.00
dht11-hum    2025-11-06T22:02:48.444962+00:00 -> 54.00
dht11-temp   2025-11-06T22:02:48.435114+00:00 -> 21.70
dht11-hum    2025-11-06T22:02:38.166411+00:00 -> 54.00
dht11-temp   2025-11-06T22:02:38.151901+00:00 -> 21.70
dht11-hum    2025-11-06T22:02:27.885686+00:00 -> 54.00
dht11-temp   2025-11-06T22:02:27.876304+00:00 -> 21.70
dht11-hum    2025-11-06T22:02:17.607088+00:00 -> 54.00
dht11-temp   2025-11-06T22:02:17.593329+00:00 -> 21.70
dht11-hum    2025-11-06T22:02:07.326679+00:00 -> 54.00
dht11-temp   2025-11-06T22:02:07.316332+00:00 -> 21.70
dht11-hum    2025-11-06T22:01:57.048618+00:00 -> 54.00
dht11-temp   2025-11-06T22:01:57.038797+00:00 -> 21.70
dht11-hum    2025-11-06T22:01:46.767455+00:00 -> 54.00
dht11-temp   2025-11-06T22:01:46.754331+00:00 -> 21.70
dht11-hum    2025-11-06T22:01:36.487813+00:00 -> 54.00
dht11-temp   2025-11-06T22:01:36.478502+00:00 -> 21.70
dht11-hum    2025-11-06T22:01:26.211676+00:00 -> 54.00
dht11-temp   2025-11-06T22:01:26.198644+00:00 -> 21.70
dht11-hum    2025-11-06T22:01:15.933499+00:00 -> 54.00
dht11-hum    2025-11-06T22:01:05.666793+00:00 -> 54.00
dht11-temp   2025-11-06T22:01:05.653905+00:00 -> 21.70
dht11-hum    2025-11-06T22:00:55.385721+00:00 -> 54.00
dht11-temp   2025-11-06T22:00:55.375335+00:00 -> 21.70
dht11-hum    2025-11-06T22:00:45.106785+00:00 -> 54.00
dht11-temp   2025-11-06T22:00:45.097110+00:00 -> 21.80
dht11-hum    2025-11-06T22:00:34.830256+00:00 -> 55.00
dht11-temp   2025-11-06T22:00:34.817845+00:00 -> 21.80
dht11-hum    2025-11-06T22:00:24.551758+00:00 -> 55.00
dht11-temp   2025-11-06T22:00:24.542294+00:00 -> 21.80
dht11-hum    2025-11-06T22:00:14.275618+00:00 -> 55.00
dht11-temp   2025-11-06T22:00:14.266136+00:00 -> 21.80
dht11-hum    2025-11-06T22:00:04.000558+00:00 -> 55.00
dht11-temp   2025-11-06T22:00:03.987893+00:00 -> 21.80
dht11-hum    2025-11-06T21:59:53.719643+00:00 -> 55.00
dht11-temp   2025-11-06T21:59:53.708461+00:00 -> 21.80
dht11-hum    2025-11-06T21:59:43.441420+00:00 -> 55.00
dht11-hum    2025-11-06T21:59:33.175095+00:00 -> 55.00
dht11-temp   2025-11-06T21:59:33.157171+00:00 -> 21.80
dht11-hum    2025-11-06T21:59:22.891520+00:00 -> 55.00
dht11-temp   2025-11-06T21:59:22.881899+00:00 -> 21.80
dht11-hum    2025-11-06T21:59:12.614675+00:00 -> 55.00
dht11-temp   2025-11-06T21:59:12.604195+00:00 -> 21.80
dht11-hum    2025-11-06T21:59:02.338286+00:00 -> 55.00
dht11-temp   2025-11-06T21:59:02.325306+00:00 -> 21.80
dht11-hum    2025-11-06T21:58:52.060107+00:00 -> 55.00
dht11-temp   2025-11-06T21:58:52.049883+00:00 -> 21.80
dht11-hum    2025-11-06T21:58:41.782497+00:00 -> 55.00
dht11-temp   2025-11-06T21:58:41.770779+00:00 -> 21.80
dht11-hum    2025-11-06T21:58:31.502679+00:00 -> 55.00
dht11-hum    2025-11-06T21:58:21.234565+00:00 -> 55.00
dht11-temp   2025-11-06T21:58:21.223078+00:00 -> 21.80
dht11-hum    2025-11-06T21:58:10.956160+00:00 -> 55.00
dht11-temp   2025-11-06T21:58:10.943430+00:00 -> 21.80
dht11-hum    2025-11-06T21:58:00.677612+00:00 -> 55.00
dht11-temp   2025-11-06T21:58:00.667103+00:00 -> 21.80
dht11-hum    2025-11-06T21:57:50.397150+00:00 -> 56.00
dht11-temp   2025-11-06T21:57:50.387929+00:00 -> 21.80
dht11-hum    2025-11-06T21:57:40.122832+00:00 -> 56.00
dht11-temp   2025-11-06T21:57:40.111877+00:00 -> 21.80
dht11-hum    2025-11-06T21:57:29.844113+00:00 -> 56.00
dht11-temp   2025-11-06T21:57:29.833747+00:00 -> 21.80
dht11-hum    2025-11-06T21:57:19.566493+00:00 -> 56.00
dht11-temp   2025-11-06T21:57:19.554601+00:00 -> 21.80
dht11-hum    2025-11-06T21:57:09.288731+00:00 -> 56.00
dht11-temp   2025-11-06T21:57:09.278474+00:00 -> 21.80
dht11-hum    2025-11-06T21:56:59.011169+00:00 -> 56.00
dht11-temp   2025-11-06T21:56:58.999201+00:00 -> 21.80
dht11-hum    2025-11-06T21:56:48.729956+00:00 -> 56.00
dht11-temp   2025-11-06T21:56:48.713590+00:00 -> 21.80
dht11-hum    2025-11-06T21:56:38.439215+00:00 -> 56.00

=== Promedios por minuto (10 minutos) ===
dht11-hum    2025-11-06 22:06:00 -> 53.00
dht11-hum    2025-11-06 22:05:00 -> 53.00
dht11-hum    2025-11-06 22:04:00 -> 53.67
dht11-hum    2025-11-06 22:03:00 -> 54.00
dht11-hum    2025-11-06 22:02:00 -> 54.00
dht11-hum    2025-11-06 22:01:00 -> 54.00
dht11-hum    2025-11-06 22:00:00 -> 54.67
dht11-hum    2025-11-06 21:59:00 -> 55.00
dht11-hum    2025-11-06 21:58:00 -> 55.00
dht11-hum    2025-11-06 21:57:00 -> 56.00
dht11-hum    2025-11-06 21:56:00 -> 56.00
dht11-temp   2025-11-06 22:06:00 -> 21.70
dht11-temp   2025-11-06 22:05:00 -> 21.70
dht11-temp   2025-11-06 22:04:00 -> 21.70
dht11-temp   2025-11-06 22:03:00 -> 21.70
dht11-temp   2025-11-06 22:02:00 -> 21.70
dht11-temp   2025-11-06 22:01:00 -> 21.70
dht11-temp   2025-11-06 22:00:00 -> 21.78
dht11-temp   2025-11-06 21:59:00 -> 21.80
dht11-temp   2025-11-06 21:58:00 -> 21.80
dht11-temp   2025-11-06 21:57:00 -> 21.80
dht11-temp   2025-11-06 21:56:00 -> 21.80
```