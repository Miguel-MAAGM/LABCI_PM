import numpy as np
import matplotlib.pyplot as plt

# Datos medidos
frecuencias = np.array([10, 50, 100, 200, 300, 400, 450, 600, 800, 1000])  # Hz
vpp = np.array([0.9, 0.89, 0.85, 0.78, 0.71, 0.65, 0.636, 0.5, 0.35, 0.2])  # Vpp medido

# Valor de referencia a baja frecuencia
vpp_0 = vpp[0]

# Ganancia en dB
ganancia_db = 20 * np.log10(vpp / vpp_0)

# Frecuencia de corte
fc = 450  # Hz

# Gráfico
plt.figure(figsize=(8, 5))
plt.semilogx(frecuencias, ganancia_db, marker='o', label='Ganancia medida [dB]')
plt.axhline(-3, color='red', linestyle='--', label='-3 dB')
plt.axvline(fc, color='green', linestyle='--', label='Frecuencia de corte: 450 Hz')
plt.title('Respuesta en frecuencia (medida)')
plt.xlabel('Frecuencia [Hz]')
plt.ylabel('Ganancia [dB]')
plt.grid(True, which='both')
plt.legend()
plt.tight_layout()
plt.show()
