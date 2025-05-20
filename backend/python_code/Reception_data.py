import serial
import struct
import time

# Configuración del puerto serie
puerto_serie = serial.Serial('COM7', 9600)  # Ajusta el nombre del puerto COM según sea necesario

# Estructura para almacenar los datos recibidos
class Payload:
    def __init__(self):
        self.raw = [0, 0, 0, 0, 0, 0]

# Bucle principal
try:
    while True:
        tiempo_inicio = time.perf_counter()

        # Leer 6 bytes desde el puerto serie
        datos = puerto_serie.read(6)

        # Verificar si se han recibido suficientes datos
        if len(datos) == 6:
            # Desempaquetar los datos en la estructura Payload
            pyload = Payload()
            pyload.raw = list(datos)

            # Verificar la marca de inicio y fin
            if pyload.raw[0] == 0xFF and pyload.raw[5] == 0xFF:
                # Obtener los valores CH1 y CH2
                CH1 = struct.unpack('<H', bytes(pyload.raw[1:3]))[0]
                CH2 = struct.unpack('<H', bytes(pyload.raw[3:5]))[0]

                # Calcular el tiempo transcurrido desde la última lectura
                tiempo_fin = time.perf_counter()
                tiempo_transcurrido = tiempo_fin - tiempo_inicio

                # Mostrar los valores recibidos y el tiempo transcurrido
                print(f'CH1: {CH1}, CH2: {CH2}, Tiempo transcurrido: {tiempo_transcurrido} segundos')

except KeyboardInterrupt:
    # Cerrar el puerto serie al salir
    puerto_serie.close()
    print("Programa terminado.")
