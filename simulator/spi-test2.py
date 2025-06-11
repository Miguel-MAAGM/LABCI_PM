import numpy as np
import matplotlib.pyplot as plt
# Parámetros de ejemplo
frecuencias = [1e6, 5e6, 10e6]  # en Hz
payload = np.array([1, 10, 50, 100, 255])  # bytes

for f in frecuencias:
    # Tiempo de transmisión pura en µs
    tx_time = payload * 8 / f * 1e6  
    # Supongamos un overhead fijo de 50 µs
    latency = 50 + tx_time
    plt.plot(payload, latency, label=f"{f/1e6:.0f} MHz")

plt.xlabel("Payload (bytes)")
plt.ylabel("Latencia round-trip (µs)")
plt.legend()
plt.show()