#include <cmath>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <semaphore.h>
#include <cstring>
#include <iostream>
#include <chrono>
#include <thread>

const char* SHM_NAME = "/senoidal";
const char* SEM_NAME = "/sem_seno";
const size_t CHUNK_SIZE = 50;
const size_t SHM_SIZE = CHUNK_SIZE * sizeof(float);

int main() {
    // Crear memoria compartida
    int fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    ftruncate(fd, SHM_SIZE);
    void* ptr = mmap(nullptr, SHM_SIZE, PROT_WRITE, MAP_SHARED, fd, 0);
    float* buffer = static_cast<float*>(ptr);

    // Crear semáforo con valor inicial 0
    sem_t* sem = sem_open(SEM_NAME, O_CREAT, 0666, 0);
    if (sem == SEM_FAILED) {
        perror("sem_open");
        return 1;
    }

    int contador = 0;
    while (true) {
        // Generar chunk senoidal
        for (int i = 0; i < CHUNK_SIZE; ++i) {
            buffer[i] = sin(2 * M_PI * i / CHUNK_SIZE + contador * 0.1f);
        }
        
        // Solo postea si no hay señal pendiente
        int sval;
        sem_getvalue(sem, &sval);
        if (sval == 0) {
            sem_post(sem);
            std::cout <<" FIRST DATA " <<buffer[0] << " "<< std::endl;
            std::cout << "[C++] Chunk #" << contador << " posteado\n";
        } else {
            std::cout <<" FIRST DATA " <<buffer[0] << " "<< std::endl;

            std::cout << "[C++] Chunk #" << contador << " descartado (esperando consumo)\n";
        }

        contador++;
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }

    munmap(ptr, SHM_SIZE);
    close(fd);
    sem_close(sem);
    return 0;
}
