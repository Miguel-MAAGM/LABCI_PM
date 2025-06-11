import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Datos extraídos manualmente del mensaje
grados = np.array([
    -180, -170, -160, -150, -140, -130, -120, -110, -100, -90, -80, -70, -60,
    -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110,
    120, 130, 140, 150, 160, 170, 180
])

voltaje_A = np.array([
    0.11, 0.132, 0.2, 0.3, 0.41, 0.505, 0.626, 0.735, 0.831, 0.941, 1.05, 1.14, 1.26,
    1.36, 1.46, 1.57, 1.68, 1.76, 1.82, 1.8, 1.75, 1.62, 1.52, 1.43, 1.3, 1.21, 1.1,
    0.982, 0.896, 0.783, 0.678, 0.57, 0.46, 0.343, 0.255, 0.17, 0.11
])

voltaje_B = np.array([
    0.11, 0.122, 0.193, 0.297, 0.4, 0.501, 0.619, 0.729, 0.822, 0.935, 1.03, 1.14, 1.25,
    1.35, 1.45, 1.56, 1.66, 1.76, 1.81, 1.78, 1.71, 1.62, 1.51, 1.4, 1.3, 1.21, 1.1,
    0.983, 0.89, 0.779, 0.667, 0.569, 0.457, 0.343, 0.25, 0.157, 0.1
])

# Determinar el mínimo y máximo para área

offset = 0.05
voltaje_B_offset = voltaje_B + offset

# Recalcular límites inferior y superior para el área de confianza
lower_offset = np.minimum(voltaje_A, voltaje_B_offset)
upper_offset = np.maximum(voltaje_A, voltaje_B_offset)

# Graficar con desfase
plt.figure(figsize=(10, 6))
plt.fill_between(grados, lower_offset, upper_offset, color='gray', alpha=0.5, label='Banda de confianza')
plt.xlabel('Diferencia de Fase (Grados)')
plt.ylabel('Voltaje (V)')
plt.title('Curva de Fase con Desfase y Banda de Confianza')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()