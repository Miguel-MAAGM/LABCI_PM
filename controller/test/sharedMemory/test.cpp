#include <cmath>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <cstring>
#include <iostream>

int main() {
    const char* shm_name = "/senoidal";
    const size_t num_floats = 256;
    const size_t size = num_floats * sizeof(float);

    // Crear y truncar la memoria compartida
    int fd = shm_open(shm_name, O_CREAT | O_RDWR, 0666);
    if (fd == -1) {
        perror("shm_open");
        return 1;
    }

    if (ftruncate(fd, size) == -1) {
        perror("ftruncate");
        return 1;
    }

    // Mapear la memoria
    void* ptr = mmap(nullptr, size, PROT_WRITE, MAP_SHARED, fd, 0);
    if (ptr == MAP_FAILED) {
        perror("mmap");
        return 1;
    }

    float* buffer = static_cast<float*>(ptr);

    // Escribir la señal senoidal
    for (size_t i = 0; i < num_floats; ++i) {
        buffer[i] = std::sin(2 * M_PI * i / num_floats);  // 1 ciclo
    }

    std::cout << "Señal senoidal escrita en memoria compartida." << std::endl;

    // Liberar
    munmap(ptr, size);
    close(fd);

    return 0;
}
