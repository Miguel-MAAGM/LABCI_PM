import asyncio
import mmap
import posix_ipc
import struct
import websockets
import json
import threading

SHM_NAME = "/senoidal"
SEM_NAME = "/sem_seno"
CHUNK_SIZE = 50
SHM_SIZE = CHUNK_SIZE * 4

# Cola para compartir entre hilos
latest_chunk = None
lock = threading.Lock()

def lector_memoria():
    global latest_chunk

    # Abrir memoria compartida
    shm = posix_ipc.SharedMemory(SHM_NAME)
    map_file = mmap.mmap(shm.fd, SHM_SIZE, mmap.MAP_SHARED, mmap.PROT_READ)
    shm.close_fd()

    # Abrir semáforo
    sem = posix_ipc.Semaphore(SEM_NAME)

    print("[Servidor] Lector iniciado...")

    while True:
        sem.acquire()
        map_file.seek(0)
        raw = map_file.read(SHM_SIZE)
        data = struct.unpack(f'{CHUNK_SIZE}f', raw)
        print(f"[Servidor] Chunk capturado: {len(data)}")
        with lock:
            latest_chunk = data


# Servidor WebSocket
async def handler(websocket):
    await websocket.send(json.dumps({"status": "conectado"}))
    while True:
        await asyncio.sleep(0.1)  # espera regular
        with lock:
            if latest_chunk:
                
                await websocket.send(json.dumps({"datos": latest_chunk}))

async def main():
    print("[Servidor] WebSocket escuchando en ws://0.0.0.0:8765")
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever

# Iniciar hilo de lectura de memoria
threading.Thread(target=lector_memoria, daemon=True).start()

# Lanzar el servidor WebSocket
asyncio.run(main())
