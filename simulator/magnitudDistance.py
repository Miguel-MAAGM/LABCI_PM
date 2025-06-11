import numpy as np
import matplotlib.pyplot as plt

# Parámetros del sistema
r = 0.5                  # Radio del plato (m)
delta_x = 0           # Desfase del transmisor en X (m)
receiver = np.array([1.0, 0.0])  # Posición fija del receptor (m)
wavelength = 0.005       # Longitud de onda (m) → 60 GHz

# Ángulos de desplazamiento del disco (0° a 359°)
angles_deg = np.arange(0, 360, 1)
angles_rad = np.radians(angles_deg)

# Arrays para resultados
distances = np.zeros_like(angles_rad, dtype=float)
magnitudes = np.zeros_like(angles_rad, dtype=float)
phase_wrapped_deg = np.zeros_like(angles_rad, dtype=float)

# Cálculo
for i, theta in enumerate(angles_rad):
    tx_x = r * np.cos(theta) + delta_x
    tx_y = r * np.sin(theta)
    d = np.hypot(receiver[0] - tx_x, receiver[1] - tx_y)
    distances[i] = d
    magnitudes[i] = 1 / d
    phase_rad = -2 * np.pi * d / wavelength
    # Envolver fase en [0, 360)
    phase_deg = np.degrees(phase_rad)
    phase_wrapped_deg[i] = phase_deg % 360

# Graficar
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10), sharex=True)

# Magnitud vs ángulo
ax1.plot(angles_deg, magnitudes, label='Magnitud (1/d)')
ax1.set_ylabel('Magnitud relativa')
ax1.set_title('Magnitud vs Ángulo de Giro')
ax1.grid(True)
ax1.legend()

# Fase absoluta (wrapped) vs ángulo
ax2.plot(angles_deg, phase_wrapped_deg, label='Fase absoluta (°)', linewidth=1.5)
ax2.set_xlabel('Ángulo de giro (°)')
ax2.set_ylabel('Fase (°)')
ax2.set_title('Fase envuelta (0–360°) vs Ángulo de Giro')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()
