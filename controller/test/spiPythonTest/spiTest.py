import spidev
import time

# Inicializar SPI
spi = spidev.SpiDev()
try:
    spi.open(1, 1)  # Bus 0, CS0
except FileNotFoundError:
    print("No se encontró el dispositivo SPI. Asegúrate de que el bus SPI esté habilitado.")
    exit(1)
spi.max_speed_hz = 1000000  # 10 MHz
spi.mode = 0b00  # SPI mode 0
spi.bits_per_word = 8

# Paso 1: Enviar 4 bytes al STM32
tx_data = [0xA1, 0xB2, 0xC3, 0x7E]
rx_data = spi.xfer2(tx_data)
print("Primer envío - RX del STM32:", rx_data)

# Esperar un poco para que STM32 prepare la respuesta
time.sleep(0.01)

# Paso 2: Enviar 4 bytes dummy para leer la respuesta del STM32
dummy = [0x00, 0x00, 0x00, 0x00]
response = spi.xfer2(dummy)
print("Segundo envío - Respuesta del STM32:", response)