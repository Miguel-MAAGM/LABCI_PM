#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
#include <string.h>

#define SPI_DEVICE "/dev/spidev1.1"  // Asegúrate que este dispositivo exista
#define SPI_SPEED 1000000            // 1 MHz
#define ACK_EXPECTED 0xAC

int main() {
    int fd = open(SPI_DEVICE, O_RDWR);
    if (fd < 0) {
        perror("Error abriendo SPI");
        return 1;
    }

    uint8_t mode = SPI_MODE_0;
    uint8_t bits = 8;
    uint32_t speed = SPI_SPEED;

    // Configuración SPI
    ioctl(fd, SPI_IOC_WR_MODE, &mode);
    ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
    ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);

    // Ingreso del valor
    char input_hex[10];
    printf("Ingrese valor a enviar (hex, sin 0x): ");
    scanf("%s", input_hex);
    uint16_t valor = (uint16_t)strtol(input_hex, NULL, 16);

    // Separar en bytes
    uint8_t paquete_tx[4];
    uint8_t paquete_rx[4] = {0};

    paquete_tx[0] = 0xB1;
    paquete_tx[1] = valor & 0xFF;         // LSB
    paquete_tx[2] = (valor >> 8) & 0xFF;  // MSB
    paquete_tx[3] = 0x00;  // Dummy para leer ACK

    struct spi_ioc_transfer tr = {
        .tx_buf = (unsigned long)paquete_tx,
        .rx_buf = (unsigned long)paquete_rx,
        .len = 4,
        .delay_usecs = 0,
        .speed_hz = speed,
        .bits_per_word = bits,
        .cs_change = 0,
    };

    // Transferencia SPI
    int ret = ioctl(fd, SPI_IOC_MESSAGE(1), &tr);
    if (ret < 1) {
        perror("Falló transferencia SPI");
        close(fd);
        return 1;
    }

    // Mostrar resultados
    printf("TX: ");
    for (int i = 0; i < 4; i++) printf("0x%02X ", paquete_tx[i]);
    printf("\nRX: ");
    for (int i = 0; i < 4; i++) printf("0x%02X ", paquete_rx[i]);
    printf("\n");

    if (paquete_rx[3] == ACK_EXPECTED) {
        printf("✔️ ACK 0x%X recibido correctamente\n", ACK_EXPECTED);
    } else {
        printf("❌ ACK inválido o no recibido (0x%02X)\n", paquete_rx[3]);
    }

    close(fd);
    return 0;
}
