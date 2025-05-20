import asyncio
import websockets
import struct
import json
import serial


# Configuración del puerto serie
puerto_serie = serial.Serial('/dev/ttyACM0', 115200)  # Ajusta el nombre del puerto COM según sea necesario

# Estructura para almacenar los datos recibidos
class Payload:
    def __init__(self):
        self.raw = [0, 0, 0, 0, 0, 0]

data_x=[]
data_y=[]
count=0
# Lista de clientes conectados
clientes = set()

async def enviar_datos_a_clientes(datos):
    if clientes:
        # Convertir los datos a formato JSON
        datos_json = json.dumps(datos)

        # Enviar datos a todos los clientes
        await asyncio.gather(*(cliente.send(datos_json) for cliente in clientes))

async def recibir_datos(websocket, path):
    global clientes
    clientes.add(websocket)

    try:
        global count
        global data_x
        global data_y
        while True:
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
                    data_x.append(CH1)
                    data_y.append(CH2)
                    count=count+1
                    # Calcular el tiempo transcurrido desde la última lectura
                    tiempo_transcurrido = asyncio.get_event_loop().time()
                    if count>40:
                        promedioCh1 = sum(data_x) / len(data_x)
                        promedioCh2 = sum(data_y) / len(data_y)
                        datos = {"CH1": promedioCh1, "CH2": promedioCh2, "Tiempo": tiempo_transcurrido}
                   # Enviar datos a todos los clientes conectados
                        count=0
                        data_y=[]
                        data_x=[]
                        await enviar_datos_a_clientes(datos)

                    # Crear un diccionario con los datos

    except websockets.exceptions.ConnectionClosedError:
        pass
    finally:
        # Remover el cliente al desconectar
        clientes.remove(websocket)

start_server = websockets.serve(recibir_datos, "192.168.1.119", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
