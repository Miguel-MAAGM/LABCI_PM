import threading
import mmap
import posix_ipc
import struct
import queue
import time

SHM_NAME = "/senoidal"
SEM_NAME = "/sem_seno"
CHUNK_SIZE = 50
SHM_SIZE = CHUNK_SIZE * 4  # 4 bytes por float

# Cola para distribuir los datos
data_queue = queue.Queue()

def lector():
    shm = posix_ipc.SharedMemory(SHM_NAME)
    map_file = mmap.mmap(shm.fd, SHM_SIZE, mmap.MAP_SHARED, mmap.PROT_READ)
    shm.close_fd()
    sem = posix_ipc.Semaphore(SEM_NAME)

    while True:
        sem.acquire()  # Esperar a que C++ indique que hay datos

        map_file.seek(0)
        raw = map_file.read(SHM_SIZE)
        chunk = struct.unpack(f'{CHUNK_SIZE}f', raw)

        # Enviar a la cola
        data_queue.put(chunk)
        print(f"{chunk}")
        print("[Lector] Chunk capturado y encolado")

# Iniciar hilo lector
if __name__ == "__main__":
    lector()
