import mmap
import posix_ipc
import struct

SHM_NAME = "/senoidal"
FLOAT_COUNT = 256
SHM_SIZE = FLOAT_COUNT * 4  # 4 bytes por float

# Abrir la memoria compartida
shm = posix_ipc.SharedMemory(SHM_NAME)
map_file = mmap.mmap(shm.fd, SHM_SIZE, mmap.MAP_SHARED, mmap.PROT_READ)
shm.close_fd()  # Ya no se necesita el descriptor

# Leer los datos como 256 floats
raw = map_file.read(SHM_SIZE)
data = struct.unpack('256f', raw)

print("Señal leída desde la memoria compartida:")
for i, val in enumerate(data[:10]):
    print(f"data[{i}] = {val:.4f}")

map_file.close()
